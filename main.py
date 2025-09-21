import urllib.request
import requests


def main():
    print("Добро пожаловать в http-клиент!\n")
    while True:
        print("Введите url")
        url = input()
        print("Выдите метод запроса (get, post, put, delete)")
        method = input().lower()
        while method not in ["get", "post", "put", "delete"]:
            print("Попробуйте еще раз")
            print("Введите один из методов: get, post, put, delete")
            method = input().lower()
        match method:
            case "get":
                with requests.get(url, headers={"hane":"qwe"}) as fp:

                # break
            case "put":
                "TODO"
            case "post":
                "TODO"
            case "delete":
                "TODO"






if __name__ == "__main__":
    main()