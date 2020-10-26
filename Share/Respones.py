
from django.http import JsonResponse, HttpResponse

# 自定义状态码
class HttpCode(object):
    # 正常登陆
    ok = 0
    # 参数错误
    paramserror = 400
    # 权限错误
    unauth = 401
    # 方法错误
    methoderror = 405
    # 服务器内部错误
    servererror = 500


# 定义统一的 json 字符串返回格式
def result(code=HttpCode.ok, message="", data=None,**kwargs):
    json_dict = {"code": code, "data": data, "msg": message}
    if kwargs and isinstance(kwargs, dict):
        json_dict.update(kwargs)
    return JsonResponse(json_dict)


def success(message="", data=None, **kwargs):
    return result(code=HttpCode.ok, data=data, message=message,**kwargs)


# 参数错误
def params_error(message="", data=None, kwargs=None):
    return result(code=HttpCode.paramserror, data=data, message=message,kwargs=kwargs)


# 权限错误
def unauth(message="", data=None, kwargs=None):
    return result(code=HttpCode.unauth, data=data, message=message)


# 方法错误
def method_error(code=HttpCode.methoderror, message="", data=None, kwargs=None):
    return result(code=code, data=data, message=message)

# 服务器内部错误


def server_error(message="", data=None, kwargs=None):
    return result(code=HttpCode.servererror, data=data, message=message)