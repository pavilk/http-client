import requests
import json
from client import Client
import http_request
import re
from cli import ArgParser


def main():
    print("Добро пожаловать в http-клиент!\n")

    Client.load_cookies()

    args = ArgParser.parse(ArgParser())

    url = args.url or input("Введите url")
    method = (args.method or input("Введите метод (get, post, put, delete)").strip().lower())
    headers = args.headers or read_json_input("Ведите заголовки в формате JSON или Enter")
    body = args.headers or read_json_input("Ведите тело в формате JSON или Enter")
    timeout = args.timeout
    if timeout is None:
        timeout_input = input("Введите таймаут (в секундах) или Enter").strip()
        timeout = float(timeout_input) if timeout_input else None

    filename = args.filename or input("Введите имя файла для сохранения ответа или Enter").strip() or None

    request = http_request.HttpRequest(method, url, headers, body, timeout=timeout, filename=filename)
    Client.send(request)

    print_response(request.response)


def print_response(response: requests.Response):
    print("===RESPONSE===")
    print(response.status_code)
    for k in response.headers:
        print(f"{k}: {response.headers[k]}")
    print("\nBody")
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
