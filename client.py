import requests
import json
from http_request import HttpRequest


class Client:
    session = requests.Session()
    cookie_file = "cookie.json"

    @staticmethod
    def load_cookies():
        try:
            with open(Client.cookie_file, "r") as f:
                cookies = json.load(f)
                Client.session.cookies.update(cookies)
        except FileNotFoundError:
            print("Cookie-файл не найден")

    @staticmethod
    def save_cookies():
        with open(Client.cookie_file, "w") as f:
            json.dump(Client.session.cookies.get_dict(), f, indent=2)

    @staticmethod
    def send(request: HttpRequest):
        try:
            response = Client.session.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                data=request.body,
                timeout=request.timeout
            )
            request.response = response

            if request.filename:
                request.save_response_in_file()

            Client.save_cookies()

            return response

        except requests.exceptions.RequestException as err:
            print("Ошибка при выполнении запроса")
            print("Ответ сервера:")
            print(err.response)
