import requests
import json
import time
from tqdm import tqdm
from http_request import HttpRequest
from requests.auth import HTTPBasicAuth
import websockets
import websocket

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
    def send(request: HttpRequest, auth: HTTPBasicAuth = None):
        with Client.session.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                data=request.body,
                timeout=request.timeout,
                allow_redirects=True,
                auth=auth,
                stream=True,
        ) as response:
            request.response = response
            chunk_size = 1024
            content = bytearray()

            total = response.headers.get('content-length')
            if total is not None:
                total = int(total)
                desc = f"Downloading {request.url}"
                with tqdm(total=total, unit='B', unit_scale=True, desc=desc) as pbar:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            content.extend(chunk)
                            pbar.update(len(chunk))
            else:
                desc = f"Downloading {request.url} (chunked)"
                with tqdm(unit='B', unit_scale=True, desc=desc) as pbar:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            content.extend(chunk)
                            pbar.update(len(chunk))

            request.response._content = content

            if request.filename:
                request.save_response_in_file()

            Client.save_cookies()
            return response

    @staticmethod
    def retry(request: HttpRequest, auth: HTTPBasicAuth = None):
        max_retry_count = 5
        max_delay_ms = 1000
        delay_base_ms = 50

        attempt_count = 0
        max_attempt_count = max_retry_count + 1

        while attempt_count < max_attempt_count:
            result = Client.send(request, auth)
            attempt_count += 1
            if not str(result.status_code).startswith('5'):
                return

            delay = min(delay_base_ms * pow(2, attempt_count), max_delay_ms)
            time.sleep(delay)

    @staticmethod
    def run_websocket_client(url):
        ws = websockets.connect(url)

        while True:
            to_send = input("Введите сообщение (или /exit): ")

            if to_send == "/exit":
                ws.close()
                break

            ws.send(to_send)

            try:
                response = ws.recv()
                print("Ответ:", response)
            except websockets.ConnectionClosed:
                print("Соединение закрыто сервером")
                break
