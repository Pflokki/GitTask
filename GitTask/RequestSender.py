from requests import Session, Response
from GitTask.ResponseError import ParameterError, TokenError

import datetime


def rate_limit(func):
    def wrapper(*args, **kwargs):
        ret_value = func(*args, **kwargs)

        if isinstance(ret_value, Response):
            if ret_value.status_code == 403:
                rate_limit_value: int = int(ret_value.headers.get('X-Ratelimit-Reset', None))
                if rate_limit:
                    print(f"Rate limit reached, unlock time is: "
                          f"{datetime.datetime.fromtimestamp(rate_limit_value).strftime('%Y-%m-%d %H:%M:%S')}")
            elif ret_value.status_code != 200:
                print(ret_value.status_code, ret_value.content)
        return ret_value
    return wrapper


def token_error_handler(func):
    def wrapper(*args, **kwargs):
        ret_value = func(*args, **kwargs)

        for value in ret_value:
            if isinstance(value, Response):
                if value.status_code == 401:
                    raise TokenError
        return ret_value
    return wrapper


def parameters_error_handler(func):
    def wrapper(*args, **kwargs):
        ret_value = func(*args, **kwargs)

        for value in ret_value:
            if isinstance(value, Response):
                if value.status_code == 404:
                    raise ParameterError
        return ret_value
    return wrapper


class RequestSender:
    @staticmethod
    @rate_limit
    @token_error_handler
    @parameters_error_handler
    def send(request):
        with Session() as s:
            resp = s.send(request.prepare())
        return resp
