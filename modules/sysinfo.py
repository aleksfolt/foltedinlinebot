import psutil
import platform
import requests
from aiogram.enums import ParseMode
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib
import GPUtil  # Необходимо установить библиотеку `gputil`
import os


def get_system_info():
    # Информация о RAM и Swap
    ram = psutil.virtual_memory()
    ram_total = ram.total / (1024 ** 3)
    ram_used = ram.used / (1024 ** 3)
    ram_percent = ram.percent

    swap = psutil.swap_memory()
    swap_total = swap.total / (1024 ** 3)
    swap_used = swap.used / (1024 ** 3)
    swap_percent = swap.percent

    # Информация о процессоре
    cpu_name = platform.processor()
    cpu_load = psutil.cpu_percent(interval=1)

    # Информация о диске
    disk = psutil.disk_usage('/')
    disk_total = disk.total / (1024 ** 3)
    disk_used = disk.used / (1024 ** 3)
    disk_percent = disk.percent

    # Сетевая информация
    net_info = psutil.net_if_addrs()
    net_io = psutil.net_io_counters()
    network_type = None
    ip_address = None

    for interface_name, interface_addresses in net_info.items():
        for address in interface_addresses:
            if interface_name.startswith('eth') or interface_name.startswith('wlan'):
                network_type = "Ethernet" if interface_name.startswith('eth') else "Wi-Fi"
                ip_address = address.address
                break

    # Информация о видеокарте
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        gpu_name = gpu.name
        gpu_load = gpu.load * 100  # В процентах
        gpu_memory_total = gpu.memoryTotal  # В МБ
        gpu_memory_used = gpu.memoryUsed  # В МБ
        gpu_temperature = gpu.temperature  # В градусах Цельсия
    else:
        gpu_name = "Не обнаружено"
        gpu_load = 0
        gpu_memory_total = 0
        gpu_memory_used = 0
        gpu_temperature = 0

    # Температура процессора
    cpu_temp = None
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            cpu_temp = temps['coretemp'][0].current

    return {
        "ram_total": ram_total,
        "ram_used": ram_used,
        "ram_percent": ram_percent,
        "swap_total": swap_total,
        "swap_used": swap_used,
        "swap_percent": swap_percent,
        "cpu_name": cpu_name,
        "cpu_load": cpu_load,
        "disk_total": disk_total,
        "disk_used": disk_used,
        "disk_percent": disk_percent,
        "network_type": network_type,
        "ip_address": ip_address,
        "gpu_name": gpu_name,
        "gpu_load": gpu_load,
        "gpu_memory_total": gpu_memory_total,
        "gpu_memory_used": gpu_memory_used,
        "gpu_temperature": gpu_temperature,
        "cpu_temperature": cpu_temp
    }


def get_country():
    try:
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip = ip_response.json().get('ip')

        if ip:
            country_response = requests.get(f'https://ipinfo.io/{ip}/json')
            country = country_response.json().get('country')
            return country
        else:
            return None
    except requests.RequestException as e:
        print(f"Ошибка получения информации: {e}")
        return None


async def inline_system_info(inline_query: InlineQuery):
    sys_info = get_system_info()
    country = get_country()

    message_text = (
        f"**🖥️ System Information**\n"
        f"💾 **RAM:** {sys_info['ram_used']:.2f} / {sys_info['ram_total']:.2f} GB ({sys_info['ram_percent']}%)\n"
        f"🔄 **Swap:** {sys_info['swap_used']:.2f} / {sys_info['swap_total']:.2f} GB ({sys_info['swap_percent']}%)\n"
        f"⚙️ **CPU:** {sys_info['cpu_name']} - {sys_info['cpu_load']}% Load\n"
        f"💽 **Disk:** {sys_info['disk_used']:.2f} / {sys_info['disk_total']:.2f} GB ({sys_info['disk_percent']}%)\n"
        f"🌐 **Network:** {sys_info['network_type']} - {sys_info['ip_address']}\n"
        f"🎮 **GPU:** {sys_info['gpu_name']} - {sys_info['gpu_load']:.1f}% Load\n"
        f"🧠 **GPU Memory:** {sys_info['gpu_memory_used']} / {sys_info['gpu_memory_total']} MB\n"
    )

    if sys_info['cpu_temperature'] is not None:
        message_text += f"🔥 **CPU Temp:** {sys_info['cpu_temperature']}°C\n"

    if sys_info['gpu_temperature'] > 0:
        message_text += f"🔥 **GPU Temp:** {sys_info['gpu_temperature']}°C\n"

    if country:
        message_text += f"🌍 **Country:** {country}\n"
    else:
        message_text += "🌍 **Country information could not be retrieved.**"

    message_text = message_text.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]') \
        .replace('(', '\\(').replace(')', '\\)').replace('~', '\\~').replace('`', '\\`') \
        .replace('>', '\\>').replace('#', '\\#').replace('+', '\\+').replace('-', '\\-') \
        .replace('=', '\\=').replace('|', '\\|').replace('{', '\\{').replace('}', '\\}') \
        .replace('.', '\\.').replace('!', '\\!')

    input_content = InputTextMessageContent(message_text=message_text, parse_mode=ParseMode.MARKDOWN)
    result_id = hashlib.md5("System Information".encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        title="System Information",
        input_message_content=input_content
    )

    return item
