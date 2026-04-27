# Pro Proxy Checker

Веб-приложение для поиска, проверки и генерации ссылок Telegram для прокси. Работает на Mac и Windows, интерфейс открывается в браузере.

![Status](https://img.shields.io/badge/Status-Working-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)

---

## Возможности

- Поиск прокси из 10+ источников (текстовые списки, API
- Сортировка по пингу — самые быстрые прокси сверху
- Кнопка "Копировать" — формат `IP:PORT` для вставки в любые программы
- Telegram-ссылки — `tg://socks?server=...` для SOCKS5 прокси

---

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/Savvy08/proxy-checker.git
cd proxy-checker
````

### 2. Создание виртуального окружения

#### macOS / Linux

```bash
python3.14 -m venv venv
source venv/bin/activate
```

#### Windows (CMD)

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> После активации в начале строки терминала появится `(venv)`

### 3. Установка зависимостей

```bash
pip install fastapi uvicorn jinja2 aiohttp beautifulsoup4 pydantic aiohttp-socks
```

---

## Запуск

```bash
python main.py
```

Сервер запустится на `http://127.0.0.1:8000`
Браузер откроется автоматически
Нажмите "Найти прокси" для начала поиска

---


---

## Как это работает

1. Сбор прокси: программа загружает списки с нескольких источников (GitHub, API, текстовые файлы)
2. Фильтрация: удаляются дубликаты, проверяется валидность IP
3. Проверка: для каждого прокси выполняется реальный запрос через него на google.com
4. Определение страны: через API ipapi.co или ip-api.com определяется страна по IP
5. Генерация ссылок: для SOCKS5 создаётся ссылка `tg://socks?server=IP&port=PORT`
6. Отображение: результаты показываются в таблице с флагами, пингом и кнопками действий

---

## Источники прокси

| Тип    | Источник             | Протоколы    |
| ------ | -------------------- | ------------ |
| GitHub | TheSpeedX/SOCKS-List | SOCKS5, HTTP |
| GitHub | monosans/proxy-list  | SOCKS5, HTTP |
| API    | proxyscrape.com      | SOCKS5, HTTP |
| API    | proxy-list.download  | SOCKS5, HTTP |
| TXT    | openproxylist.xyz    | SOCKS5, HTTP |

> Чтобы добавить свой источник, добавьте строку в список `sources` в `main.py`:

```python
("https://ссылка-на-список.txt", "socks5"),  # или "https"
```

> Источник должен отдавать прокси в формате `IP:PORT` (одна строка = один прокси)

---


---

## Решение проблем

### Ошибка `aiohttp_socks` не установлена

```bash
pip install aiohttp-socks
```


---

## Настройка

### Изменить количество проверяемых прокси

```python
to_check = unique_proxies[:40]
```

### Изменить таймаут проверки

```python
check_proxy_working(..., timeout=5.0)
```

### Добавить свои источники

```python
("https://ваш-источник.текст", "socks5")
```

---


## Поддержать проект

Если приложение оказалось полезным - поставьте звезду репозиторию


