from functools import wraps
from django.shortcuts import redirect


def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("session"):
            result = func(request, *args, **kwargs)
            return result
        else:
            return redirect('/platform/login/')
    return inner
