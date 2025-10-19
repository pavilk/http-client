import argparse
import json


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='http_client',
            description='''\
            HTTP(s)-клиент к вашим услугам!
            Можно делаеть всякие запросы, с таймаутами, кукисами, сохранять ответы в файл, заголовки указывать'''
        )
        self.parser.add_argument('-u', '--url', help="Введите URL запроса")
        self.parser.add_argument('-m', '--method', choices=["get", "post", "put", "delete"], help="Метод запроса")
        self.parser.add_argument('--headers',
                                 help="Заголовки в формате JSON (например {\"User-Agent\": \"Oper_Balet\"})")
        self.parser.add_argument('-b', '--body', help="Тело запроса в формате JSON")
        self.parser.add_argument('-t', '--timeout', type=float, help="Таймаут ожидания ответа в секундах")
        self.parser.add_argument('-f', '--filename', help="Имя файла для сохранения ответа")

    def parse(self):
        args = self.parser.parse_args()
        if args.headers:
            try:
                args.headers = json.loads(args.headers)
            except json.JSONDecodeError:
                print(f"Неправильный формат JSON в параметре --headers, заголовки пропущены")
                args.headers = None

        if args.body:
            try:
                args.body = json.loads(args.body)
            except json.JSONDecodeError:
                print(f"Неправильный формат JSON в параметре --body, заголовки пропущены")
                args.body = None

        return args
