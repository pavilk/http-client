import pytest
from unittest.mock import patch, MagicMock, mock_open
from main import read_json_input
from client import Client
from cli import ArgParser
import sys
from http_request import HttpRequest


# -------------------------
# FIXTURES
# -------------------------
@pytest.fixture
def sample_request():
    return HttpRequest(
        method="get",
        url="https://example.com",
        headers={},
        body=None,
        timeout=3,
        filename="output.txt",
    )


@pytest.fixture
def mock_response():
    resp = MagicMock()
    resp.status_code = 200
    resp.headers = {"content-length": "4"}
    resp.iter_content.return_value = [b"test"]
    resp.text = "test"
    return resp


# -------------------------
# HTTP TESTS
# -------------------------

def test_send_downloads_content(sample_request, mock_response):
    with patch("client.Client.session.request") as mock_req:
        mock_req.return_value.__enter__.return_value = mock_response
        Client.send(sample_request)
        assert sample_request.response is mock_response
        assert sample_request.response._content == b"test"


def test_save_response_in_file(sample_request, mock_response):
    sample_request.response = mock_response
    m = mock_open()
    with patch("builtins.open", m):
        sample_request.save_response_in_file()
    m.assert_called_once_with("output.txt", "w", encoding="UTF-8")
    handle = m()
    handle.write.assert_called_once_with("test")


def test_retry_stops_after_success(sample_request):
    bad_resp = MagicMock()
    bad_resp.status_code = 500
    good_resp = MagicMock()
    good_resp.status_code = 200

    with patch("client.Client.send", side_effect=[bad_resp, good_resp]) as m:
        with patch("time.sleep", return_value=None):  # <<< Мок sleep
            Client.retry(sample_request)

    assert m.call_count == 2  # остановилось после успешного ответа


def test_load_cookies():
    with patch("builtins.open", mock_open(read_data='{"a":"b"}')):
        Client.load_cookies()
    assert Client.session.cookies.get("a") == "b"


def test_save_cookies():
    Client.session.cookies.set("token", "123")
    m = mock_open()
    with patch("builtins.open", m):
        Client.save_cookies()
    m.assert_called_once_with("cookie.json", "w")


# -------------------------
# WebSocket TESTS
# -------------------------

class FakeWS:
    def __init__(self):
        self.sent = []
        self.closed = False
        self.recv_queue = ["echo1", "echo2"]

    def send(self, msg):
        self.sent.append(msg)

    def recv(self):
        if self.recv_queue:
            return self.recv_queue.pop(0)
        raise Exception("No more messages")

    def close(self):
        self.closed = True


def test_websocket_client():
    fake_ws = FakeWS()
    with patch("websockets.connect", return_value=fake_ws):
        # эмулируем ввод пользователя: два сообщения + /exit
        with patch("builtins.input", side_effect=["hi", "test", "/exit"]):
            Client.run_websocket_client("ws://example.com")
    assert fake_ws.sent == ["hi", "test"]
    assert fake_ws.closed is True


def test_read_json_input_valid(monkeypatch):
    # эмулируем корректный JSON ввод
    inputs = iter(['{"key":"value"}'])
    monkeypatch.setattr('builtins.input', lambda: next(inputs))
    result = read_json_input("Введите JSON")
    assert result == {"key": "value"}


def test_read_json_input_empty(monkeypatch):
    # эмулируем нажатие Enter (пустой ввод)
    inputs = iter([''])
    monkeypatch.setattr('builtins.input', lambda: next(inputs))
    result = read_json_input("Введите JSON")
    assert result is None


def test_read_json_input_invalid_then_valid(monkeypatch):
    # сначала ввод некорректного JSON, потом корректного
    inputs = iter(['{key:}', '{"ok":123}'])
    monkeypatch.setattr('builtins.input', lambda: next(inputs))
    result = read_json_input("Введите JSON")
    assert result == {"ok": 123}

# -------------------------
# Parser TESTS
# -------------------------


def test_parse_minimal_args():
    test_argv = ['http_client', '-u', 'https://example.com']

    with patch.object(sys, 'argv', test_argv):
        parser = ArgParser()
        args = parser.parse()

    assert args.url == 'https://example.com'
    assert args.method is None
    assert args.headers is None
    assert args.body is None
    assert args.timeout is None
    assert args.filename is None


def test_parse_invalid_headers_json(capsys):
    test_argv = ['http_client', '-u', 'https://example.com', '--headers', '{"User-Agent":}']

    with patch.object(sys, 'argv', test_argv):
        parser = ArgParser()
        args = parser.parse()

    captured = capsys.readouterr()
    assert "Неправильный формат JSON в параметре --headers" in captured.out
    assert args.headers is None