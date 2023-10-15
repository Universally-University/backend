from typing import Any
from django.http import HttpRequest
from icecream import ic
from django.contrib.auth import get_user
from django.shortcuts import HttpResponse


def unwrap(model):
    try:
        return model._wrapped
    except AttributeError:
        return model


def set_user_cookie(get_response):
    def middleware(request: HttpRequest):
        response: HttpResponse = get_response(request)
        response.set_cookie("member_ID", get_user(request).id)
        return response
    return middleware


def set_user_signed_cookie(get_response):
    def middleware(request: HttpRequest):
        response: HttpResponse = get_response(request)
        response.set_signed_cookie(
            "member_ID", get_user(request).id, request.COOKIES.get("sessionid")
        )
        return response
    return middleware
