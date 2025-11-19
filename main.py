import requests
from requests.auth import HTTPBasicAuth
import json
from client import Client
import http_request
from cli import ArgParser


user_agents = {
        "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0 Safari/537.36",
        "firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0)"
                   "Gecko/20100101 Firefox/115.0",
        "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                  "AppleWebKit/605.1.15 (KHTML, like Gecko)"
                  "Version/15.0 Safari/605.1.15",
        "default": "HTTPClient/1.0"
    }


def main():
    print("Добро пожаловать в http-клиент!\n")

    Client.load_cookies()

    args = ArgParser.parse(ArgParser())

    url = args.url or input("Введите url\n")

    if url.startswith("ws://") or url.startswith("wss://"):
        Client.run_websocket_client(url)
        return

    method = (args.method or input("Введите метод (get, post, put, delete)\n").strip().lower())
    agents = '\n'.join(user_agents.keys())
    agent = (args.method or input(f"Введите нужный user_agent {agents}\n"))
    username = input("Введите свой логин или Enter\n")
    password = input("Введите свой пароль или Enter\n")
    headers = args.headers or read_json_input("Ведите заголовки в формате JSON или Enter\n")
    body = args.headers or read_json_input("Ведите тело в формате JSON или Enter\n")
    timeout = args.timeout
    if timeout is None:
        timeout_input = input("Введите таймаут (в секундах) или Enter\n").strip()
        timeout = float(timeout_input) if timeout_input else None

    filename = args.filename or input("Введите имя файла для сохранения ответа или Enter\n").strip() or None

    if agent in user_agents.keys():
        if headers:
            headers["User-Agent"] = user_agents[agent]
        else:
            headers = {"User-Agent" : user_agents[agent]}

    request = http_request.HttpRequest(
        method,
        url,
        headers,
        body,
        timeout=timeout,
        filename=filename,
    )

    auth = None

    if username and password:
        auth = HTTPBasicAuth(username, password)

    Client.send(request, auth)

    if str(request.response.status_code).startswith('5'):
        Client.retry(request, auth)

    print_response(request.response, request.filename)


def print_response(response: requests.Response, file=None):
    print("===RESPONSE===")
    print(response.status_code)
    for k in response.headers:
        print(f"{k}: {response.headers[k]}")
    print("\nBody")
    if not file:
        print(response.text)


def read_json_input(message):
    print(message)
    answer = input()
    if not answer:
        return None
    try:
        return json.loads(answer)
    except json.decoder.JSONDecodeError:
        print("Некорректный JSON, попробоуйте еще раз")
        return read_json_input(message)


if __name__ == "__main__":
    main()
