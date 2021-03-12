from requests import Request
import os


def tokenizer(func):
    def wrapper(*args, **kwargs):
        ret_value: Request = func(*args, **kwargs)

        token = os.environ.get('TOKEN')
        if token:
            ret_value.headers['Authorization'] = f"token {token}"

        return ret_value
    return wrapper


class RequestMaker:
    def __init__(self):
        self.method = "GET"
        self.headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Mozilla/5.0',
            }
        self.url = ""
        self.params = {}

    @tokenizer
    def get_request(self):
        return Request(
            method=self.method,
            url=self.url,
            params=self.params,
            headers=self.headers
        )
