import asyncio
import time
import webbrowser
import threading
import re
import random
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import aiohttp
try:
    from aiohttp_socks import ProxyConnector
except ImportError:
    print("Установка библиотеки для проверки прокси...")
    import subprocess
    subprocess.check_call(["pip", "install", "aiohttp-socks"])
    from aiohttp_socks import ProxyConnector

app = FastAPI()

# Словарь кодов стран 
COUNTRY_FLAGS = {
    "US": "🇺🇸", "GB": "🇬🇧", "DE": "🇩🇪", "FR": "🇫🇷", "NL": "🇳🇱",
    "CA": "🇨🇦", "AU": "🇦🇺", "JP": "🇯🇵", "SG": "🇸🇬", "IN": "🇮🇳",
    "BR": "🇧🇷", "RU": "🇷🇺", "CN": "🇨🇳", "KR": "🇰🇷", "IT": "🇮🇹",
    "ES": "🇪🇸", "PL": "🇵🇱", "SE": "🇸🇪", "NO": "🇳🇴", "FI": "🇫🇮",
    "DK": "🇩🇰", "CH": "🇨🇭", "AT": "🇦🇹", "BE": "🇧🇪", "CZ": "🇨🇿",
    "UA": "🇺🇦", "TR": "🇹🇷", "IL": "🇮🇱", "AE": "🇦🇪", "ZA": "🇿🇦",
    "MX": "🇲🇽", "AR": "🇦🇷", "CL": "🇨🇱", "ID": "🇮🇩", "TH": "🇹🇭",
    "VN": "🇻🇳", "MY": "🇲🇾", "PH": "🇵🇭", "HK": "🇭🇰", "TW": "🇹🇼",
    "NZ": "🇳🇿", "IE": "🇮🇪", "PT": "🇵🇹", "GR": "🇬🇷", "RO": "🇷🇴",
    "BG": "🇧🇬", "HU": "🇭🇺", "SK": "🇸🇰", "HR": "🇭🇷", "RS": "🇷🇸",
    "UNKNOWN": "🌐"
}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Pro Proxy Checker</title>

<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = { darkMode: 'class' }
</script>

<script>
(function () {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') {
        document.documentElement.classList.add('dark');
    }
})();
</script>

<style>
.loader { border-top-color: #3b82f6; animation: spinner 1s linear infinite; }
@keyframes spinner { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.fade-in { animation: fadeIn 0.5s ease-in; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>

</head>

<body class="bg-gray-50 text-gray-800 font-sans dark:bg-gray-900 dark:text-gray-100">

<div class="container mx-auto px-4 py-8 max-w-7xl">

<header class="mb-8 flex justify-between items-center bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm">
<div>
<h1 class="text-3xl font-bold text-blue-600">Pro Proxy Checker</h1>
<p class="text-gray-500 dark:text-gray-400 text-sm mt-1">
Сбор прокси, дополнительный сайт для проверки прокси: <a href="https://proxy-seller.io/tools/proxy-checker/" target="_blank" class="text-blue-500 hover:underline">proxy-seller.io</a>
</p>
<p class="text-gray-500 dark:text-gray-400 text-sm mt-1">
By <a href="https://github.com/Savvy08" target="_blank" class="text-blue-500 hover:underline">Savvy08</a>
</p>
</div>

<div class="flex items-center gap-3">

<button onclick="loadProxies()" class="flex items-center bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow transition active:scale-95">
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-2">
<path stroke-linecap="round" stroke-linejoin="round"
d="M16.023 9.348h4.992M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"/>
</svg>
Найти прокси
</button>

<button onclick="toggleTheme()"
class="bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 p-2.5 rounded-lg transition shadow-sm">

<svg id="iconSun" xmlns="http://www.w3.org/2000/svg" fill="none"
viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
class="w-5 h-5 text-yellow-500 hidden">
<path stroke-linecap="round" stroke-linejoin="round"
d="M12 3v1.5m0 15V21m8.485-8.485h-1.5M4.515 12h-1.5m12.02 5.657l-1.06-1.06M6.343 6.343l-1.06-1.06m12.02 0l-1.06 1.06M6.343 17.657l-1.06 1.06M12 7.5a4.5 4.5 0 100 9 4.5 4.5 0 000-9z"/>
</svg>

<svg id="iconMoon" xmlns="http://www.w3.org/2000/svg" fill="none"
viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
class="w-5 h-5 text-gray-700 dark:text-gray-200">
<path stroke-linecap="round" stroke-linejoin="round"
d="M21.752 15.002A9 9 0 1112 2.25a7.5 7.5 0 009.752 12.752z"/>
</svg>

</button>
</div>
</header>

<div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-md mb-6 flex justify-between items-center border border-gray-100 dark:border-gray-700">
<div id="status" class="text-sm font-medium text-gray-600 dark:text-gray-300">
Нажмите кнопку для поиска...
</div>

<button id="copyAllBtn" onclick="copyAll()" class="hidden flex items-center bg-gray-800 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded-lg text-sm transition">
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2">
    <path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
</svg>
Скопировать все (<span id="countBadge">0</span>)
</button>
</div>

<div id="loader" class="hidden flex justify-center my-12">
<div class="loader rounded-full border-4 border-gray-200 dark:border-gray-700 h-16 w-16"></div>
</div>

<div class="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden border border-gray-100 dark:border-gray-700">
<div class="overflow-x-auto">

<table class="min-w-full leading-normal">

<thead>
<tr class="bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600">
<th class="px-4 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase">Страна</th>
<th class="px-4 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase">Протокол</th>
<th class="px-4 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase">Адрес</th>
<th class="px-4 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase">Анонимность</th>
<th class="px-4 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase">Задержка</th>
<th class="px-4 py-4 text-right text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase">Действия</th>
</tr>
</thead>

<tbody id="proxyTableBody" class="divide-y divide-gray-100 dark:divide-gray-700"></tbody>

</table>

</div>
</div>
</div>

<script>

let currentProxies = [];

async function loadProxies() {
const loader = document.getElementById('loader');
const status = document.getElementById('status');
const tbody = document.getElementById('proxyTableBody');
const copyBtn = document.getElementById('copyAllBtn');

loader.classList.remove('hidden');
tbody.innerHTML = '';
copyBtn.classList.add('hidden');
status.innerText = 'Загрузка...';
currentProxies = [];

try {
const res = await fetch('/api/proxies');
const data = await res.json();

currentProxies = data;
status.innerText = `Готово: ${data.length}`;

if (data.length) {
copyBtn.classList.remove('hidden');
document.getElementById('countBadge').innerText = data.length;
}

data.forEach(p => {
    const row = document.createElement('tr');
    row.className = 'hover:bg-gray-50 dark:hover:bg-gray-700 transition fade-in';
    
    const isSocks = p.protocol === 'socks5';
    const badgeClass = isSocks ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-200' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-200';
    const pingColor = p.ping > 1000 ? 'text-red-500' : (p.ping > 500 ? 'text-yellow-600' : 'text-green-600');
    
    // Анонимность
    const anonLevel = p.anonymity || 'Unknown';
    const anonColors = {
        'elite': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        'anonymous': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        'transparent': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        'unknown': 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    };
    
    // Кнопка копирования с иконкой
    let actions = `<button onclick="copyText(this, '${p.ip}:${p.port}')" class="inline-flex items-center text-gray-500 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 bg-gray-100 dark:bg-gray-600 hover:bg-blue-50 dark:hover:bg-gray-500 py-1.5 px-3 rounded-md text-xs font-bold transition mr-2">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
        </svg>
        Копия
    </button>`;
    
    // Кнопка Telegram для SOCKS5
    if (isSocks && p.tg_link) {
        actions = `<a href="${p.tg_link}" target="_blank" class="inline-flex items-center text-white bg-[#0088cc] hover:bg-[#0077b5] py-1.5 px-3 rounded-md text-xs font-bold mr-2 shadow-sm transition">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" class="w-4 h-4 mr-1">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.223-.548.223l.188-2.623 4.823-4.35c.192-.192-.054-.3-.297-.108L8.32 13.617l-2.96-.924c-.64-.203-.658-.64.135-.954l11.566-4.458c.538-.196 1.006.128.832.94z"/>
            </svg>
            Telegram
        </a>` + actions;
    }

    row.innerHTML = `
        <td class="px-4 py-4 whitespace-nowrap">
            <div class="flex items-center">
                <span class="text-2xl mr-2">${p.flag || '🌐'}</span>
                <span class="text-sm font-medium text-gray-700 dark:text-gray-200">${p.country || 'Unknown'}</span>
            </div>
        </td>
        <td class="px-4 py-4 whitespace-nowrap"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badgeClass}">${p.protocol.toUpperCase()}</span></td>
        <td class="px-4 py-4 whitespace-nowrap font-mono text-sm text-gray-700 dark:text-gray-300">${p.ip}:${p.port}</td>
        <td class="px-4 py-4 whitespace-nowrap"><span class="px-2 py-1 rounded-full text-xs font-medium ${anonColors[anonLevel.toLowerCase()] || anonColors['unknown']}">${anonLevel}</span></td>
        <td class="px-4 py-4 whitespace-nowrap text-sm font-bold ${pingColor}">${p.ping} ms</td>
        <td class="px-4 py-4 whitespace-nowrap text-right">${actions}</td>
    `;
    tbody.appendChild(row);
});

if(data.length === 0) {
     tbody.innerHTML = '<tr><td colspan="6" class="text-center py-8 text-gray-400 dark:text-gray-500">Рабочие прокси не найдены. Попробуйте позже.</td></tr>';
}

} catch {
status.innerText = 'Ошибка';
} finally {
loader.classList.add('hidden');
}
}

function copyText(btn, text) {
    navigator.clipboard.writeText(text);
    const originalHtml = btn.innerHTML;
    btn.innerHTML = '✅ OK!';
    btn.disabled = true;
    setTimeout(() => {
        btn.innerHTML = originalHtml;
        btn.disabled = false;
    }, 1000);
}

function copyAll() {
if(currentProxies.length === 0) return;
const allString = currentProxies.map(p => `${p.ip}:${p.port}`).join('\\n');
navigator.clipboard.writeText(allString).then(() => {
    alert(`Скопировано ${currentProxies.length} прокси!`);
});
}

function toggleTheme() {
const html = document.documentElement;
const sun = document.getElementById('iconSun');
const moon = document.getElementById('iconMoon');

html.classList.toggle('dark');

if (html.classList.contains('dark')) {
localStorage.setItem('theme', 'dark');
sun.classList.remove('hidden');
moon.classList.add('hidden');
} else {
localStorage.setItem('theme', 'light');
sun.classList.add('hidden');
moon.classList.remove('hidden');
}
}

window.addEventListener('DOMContentLoaded', () => {
const sun = document.getElementById('iconSun');
const moon = document.getElementById('iconMoon');

if (document.documentElement.classList.contains('dark')) {
sun.classList.remove('hidden');
moon.classList.add('hidden');
}
});

</script>

</body>
</html>
"""

async def get_country_info(ip: str, timeout: float = 3.0) -> dict:
    """Определяет страну по IP через бесплатный API"""
    try:
        # Используем ipapi.co (бесплатно, без ключа, 1000 запросов/день)
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.get(f'http://ipapi.co/{ip}/json/', timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    country_code = data.get('country_code', 'UNKNOWN')
                    country_name = data.get('country', 'Unknown')
                    flag = COUNTRY_FLAGS.get(country_code, '🌐')
                    return {
                        'country': country_name,
                        'country_code': country_code,
                        'flag': flag
                    }
    except:
        pass
    
    # Fallback: ip-api.com (бесплатно, 45 запросов/мин)
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.get(f'http://ip-api.com/json/{ip}', timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    country_code = data.get('countryCode', 'UNKNOWN')
                    country_name = data.get('country', 'Unknown')
                    flag = COUNTRY_FLAGS.get(country_code, '🌐')
                    return {
                        'country': country_name,
                        'country_code': country_code,
                        'flag': flag
                    }
    except:
        pass
    
    return {'country': 'Unknown', 'country_code': 'UNKNOWN', 'flag': '🌐'}

async def check_anonymity(ip: str, port: int, protocol: str, timeout: float = 5.0) -> tuple:
    """
    Проверяет прокси и определяет уровень анонимности
    Возвращает: (ping_ms, anonymity_level, country_info)
    """
    start_time = time.time()
    
    try:
        if protocol == 'socks5':
            connector = ProxyConnector.from_url(f'socks5://{ip}:{port}')
        else:
            connector = aiohttp.TCPConnector()
        
        async with aiohttp.ClientSession(
            connector=connector if protocol == 'socks5' else None,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as session:
            
            # Запрос для анонимности (возвращает информацию о запросе)
            check_url = 'http://httpbin.org/ip'
            
            if protocol == 'https':
                async with session.get(check_url, proxy=f'http://{ip}:{port}', timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    if response.status == 200:
                        data = await response.json()
                        proxy_ip = data.get('origin', '').split(',')[0].strip()
                        
                        # анонимность
                        if proxy_ip == ip:
                            anonymity = 'transparent'  # Прокси передаёт ваш IP
                        else:
                            anonymity = 'anonymous'  # Прокси скрывает IP
                    else:
                        anonymity = 'unknown'
            else:
                # Для SOCKS5
                async with session.get(check_url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    if response.status == 200:
                        data = await response.json()
                        anonymity = 'elite'  # SOCKS5 обычно elite
                    else:
                        anonymity = 'unknown'
        
        # Проверяем работоспособность через Google
        async with aiohttp.ClientSession(
            connector=ProxyConnector.from_url(f'socks5://{ip}:{port}') if protocol == 'socks5' else None,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as session:
            if protocol == 'socks5':
                async with session.get('http://www.google.com/generate_204', allow_redirects=False) as response:
                    if response.status < 500:
                        end_time = time.time()
                        ping = round((end_time - start_time) * 1000, 2)
                        # Получаем информацию о стране
                        country_info = await get_country_info(ip)
                        return ping, anonymity, country_info
            else:
                async with session.get('http://www.google.com/generate_204', proxy=f'http://{ip}:{port}', allow_redirects=False) as response:
                    if response.status < 500:
                        end_time = time.time()
                        ping = round((end_time - start_time) * 1000, 2)
                        country_info = await get_country_info(ip)
                        return ping, anonymity, country_info
                        
    except Exception as e:
        pass
    
    return -1, 'unknown', {'country': 'Unknown', 'flag': '🌐'}

def generate_tg_socks5_link(ip: str, port: int) -> str:
    return f"tg://socks?server={ip}&port={port}&user=&pass="

async def fetch_raw_list(url: str, protocol_hint: str) -> list:
    proxies = []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, ssl=False, timeout=15) as response:
                if response.status != 200: 
                    return []
                text = await response.text()
                matches = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b', text)
                for match in matches:
                    ip, port = match.split(':')
                    parts = ip.split('.')
                    if all(0 <= int(part) <= 255 for part in parts):
                        proxies.append({"ip": ip, "port": int(port), "protocol": protocol_hint})
    except Exception as e:
        pass
    return proxies

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_PAGE

@app.get("/api/proxies")
async def get_proxies():
    all_proxies = []
    
    sources = [

    # ProxyScrape API 
    ("https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=socks5&timeout=10000&country=all&format=txt", "socks5"),
    ("https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000&country=all&format=txt", "https"),

    # ProxyList.download API
    ("https://www.proxy-list.download/api/v1/get?type=socks5", "socks5"),
    ("https://www.proxy-list.download/api/v1/get?type=http", "https"),

    # OpenProxyList
    ("https://openproxylist.xyz/socks5.txt", "socks5"),
    ("https://openproxylist.xyz/http.txt", "https"),


    # Geonode API (очень хороший источник)
    ("https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc", "https"),

    # Monosans API (часто обновляется)
    ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt", "https"),
    ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt", "socks5"),

    # Proxyscan API
    ("https://www.proxyscan.io/download?type=http", "https"),
    ("https://www.proxyscan.io/download?type=socks5", "socks5"),

    # Spys.one (парсится regex'ом нормально)
    ("https://spys.me/socks.txt", "socks5"),
    ("https://spys.me/proxy.txt", "https"),

    # Proxyspace
    ("https://proxyspace.pro/http.txt", "https"),
    ("https://proxyspace.pro/socks5.txt", "socks5"),
]

    print(f"Загрузка {len(sources)} источников...")
    
    semaphore = asyncio.Semaphore(10)
    async def limited_fetch(url, proto):
        async with semaphore:
            return await fetch_raw_list(url, proto)

    tasks = [limited_fetch(url, proto) for url, proto in sources]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for res in results:
        if isinstance(res, list):
            all_proxies.extend(res)

    seen = set()
    unique_proxies = []
    for p in all_proxies:
        key = (p['ip'], p['port'])
        if key not in seen:
            seen.add(key)
            unique_proxies.append(p)

    print(f"Всего уникальных: {len(unique_proxies)}")
    
    if not unique_proxies:
        return []

    random.shuffle(unique_proxies)
    to_check = unique_proxies[:100]  # Проверяем 100 прокси
    
    print(f"Проверка {len(to_check)} прокси с определением страны...")
    
    # Проверяем прокси параллельно
    check_tasks = [check_anonymity(p['ip'], p['port'], p['protocol'], timeout=6.0) for p in to_check]
    results_checks = await asyncio.gather(*check_tasks, return_exceptions=True)
    
    final_list = []
    for i, p in enumerate(to_check):
        result = results_checks[i]
        if isinstance(result, Exception):
            continue
        
        ping_val, anonymity, country_info = result
        
        if ping_val > 0 and ping_val < 3000:
            p['ping'] = ping_val
            p['anonymity'] = anonymity
            p.update(country_info)  # Добавляем страну
            
            if p['protocol'] == 'socks5':
                p['tg_link'] = generate_tg_socks5_link(p['ip'], p['port'])
            
            final_list.append(p)
            print(f"✓ {p['flag']} {p.get('country', 'Unknown')} | {p['ip']}:{p['port']} | {ping_val}ms | {anonymity}")
            
    final_list.sort(key=lambda x: x['ping'])
    print(f"Итого рабочих: {len(final_list)}")
    return final_list

if __name__ == "__main__":
    import uvicorn
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000")
        
    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()
    
    print("Сервер запущен: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")