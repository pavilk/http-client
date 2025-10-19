class HttpRequest:
    def __init__(self, method, url, headers=None, body=None, cookies=None, timeout=None, filename=None):
        self.url = url
        self.method = method
        self.body = body
        self.cookies = cookies
        self.headers = headers
        self.timeout = timeout
        self.filename = filename
        self.response = None

    def save_response_in_file(self):
        with open(self.filename, "w", encoding="UTF-8") as f:
            f.write(self.response.text)
