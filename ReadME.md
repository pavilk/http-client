

````markdown
# HTTP Client

Универсальный HTTP/HTTPS клиент на Python с поддержкой:

- GET, POST, PUT, DELETE запросов
- Заголовков и тела запроса в формате JSON
- Таймаута и сессий с сохранением cookies
- Сохранения ответа в файл
- Прогресс-бара для больших загрузок
- Поддержки WebSocket

---

## Установка

1. Склонируйте репозиторий:

```bash
git clone https://github.com/pavilk/http-client
cd http-client
````

2. Создайте виртуальное окружение:

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

---

## Использование

Запуск клиента:

```bash
python main.py
```

Программа интерактивно спросит:

* URL запроса (`http://` или `https://`)
* HTTP-метод (`get`, `post`, `put`, `delete`)
* User-Agent (chrome, firefox, safari, default)
* Логин/пароль для Basic Auth
* Заголовки и тело в формате JSON
* Таймаут и имя файла для сохранения ответа

Пример с аргументами командной строки:

```bash
python main.py -u https://httpbin.org/get -m get --headers '{"User-Agent":"Test"}' -t 5 -f response.txt
```

---

## WebSocket

Поддержка WebSocket (`ws://` или `wss://`):

```bash
python main.py ws://echo.websocket.org
```

* После подключения можно отправлять сообщения
* Введите `/exit`, чтобы закрыть соединение

Пример работы:

```
Введите сообщение (или /exit): Hello
Ответ: Hello
Введите сообщение (или /exit): /exit
Соединение закрыто
```

---

## Прогресс-бар

Для больших загрузок используется `tqdm`. Пример при скачивании 5 МБ данных:

```
Downloading https://httpbin.org/stream-bytes/5000000 (chunked): 5.00MB [00:01, 4.5MB/s]
```

* Прогресс-бар показывает:

  * Сколько данных скачано
  * Общий размер
  * Скорость загрузки

---

## Структура проекта

```
http-client/
├─ main.py             # Точка входа
├─ client.py           # Класс Client с поддержкой HTTP и WebSocket
├─ http_request.py     # Класс HttpRequest для хранения данных запроса/ответа
├─ cli.py              # Парсер аргументов командной строки
├─ test_client.py      # Тесты для HTTP, WebSocket и утилит
├─ requirements.txt    # Зависимости проекта
└─ README.md
```

---

## Тестирование

Используется `pytest` с покрытием кода:

```bash
# Покрытие в терминале
pytest --cov=. --cov-report=term-missing

# Генерация HTML-отчета
pytest --cov=. --cov-report=html
```

После выполнения `pytest --cov-report=html` появится папка `htmlcov/`.
Открой `htmlcov/index.html` в браузере, чтобы увидеть, **какие строки кода покрыты тестами, а какие нет**.


## Особенности

* Сохраняет cookies между сессиями
* Повторные попытки при ошибках сервера (5xx)
* Возможность отправлять тело запроса и заголовки в формате JSON
* Возможность сохранять ответ в файл
* Поддержка WebSocket с интерактивным вводом
* Прогресс-бар при скачивании больших файлов

---

## Зависимости

* Python 3.11+
* requests
* tqdm
* websockets
* pytest 


