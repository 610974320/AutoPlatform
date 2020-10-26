from django.middleware.csrf import get_token
from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
import os
from Share.Paging import Paging
from Share.Route import Any_Path
from Share.VerifiCode import save_captcha, verify_code
from django.http import JsonResponse
from Platform.models import User, Project, VerifiCode, Case
from django.views.decorators.csrf import csrf_exempt
from Share.Check_Login import check_login
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from Share.Respones import success,params_error,unauth,method_error,server_error
from django.conf import settings
from rest_framework.decorators import api_view
from Share.VerifiCode import token
from Share.excuse_case import excuse_case


def get_verify(request):
    '''
    验证码试图函数
    :param request:
    :return:
    '''
    if request.method == 'GET':
        file_name = save_captcha()
        image_path = Any_Path('image', file_name)  # 图片路径
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/png")
    else:
        return JsonResponse(
            {
                "code": 0,
                "msg": "请求方式不合法"
            }
        )


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def login(request):
    '''
    登录视图函数
    :param request:
    :return:
    '''
    msg = ''
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            pwd = request.POST.get('pwd')
            code = request.POST.get('code').lower()
            actual_code = str(VerifiCode.objects.last()).lower()
            if username and pwd:
                user_info = User.objects.get(user_name=username)
                if username == user_info.user_name and pwd == user_info.password and code == actual_code:
                    request.session['session'] = 'login'    #生成登录后的键值对session
                    request.session['name'] = user_info.user_name    #将用户名称存入session数据库
                    request.session.set_expiry(7200)
                    return redirect("/platform/index/")
                elif username == user_info.user_name and pwd == user_info.password and code != actual_code:
                    msg = '验证码输入错误'
                else:
                    msg = '用户名或者密码错误'
        except Exception:
            msg = '请正确输入用户信息'
        else:
            msg = '请输入用户名或者密码'

    return render(request, "login.html", {"msg": msg})


@check_login
def index(request):
    user_name = request.session.get('name')
    data = {"user_name": user_name}
    return render(request, 'index.html', data)


@check_login
def logout(request):
    request.session.flush()
    return redirect('/platform/login/')


@check_login
def query(request):
    if request.method == "POST":
        return HttpResponse(700)



@api_view(['POST','GET'])
@check_login
def user_info(request):
    '''
    获取用户信息
    :param request:
    :return:
    '''
    import json
    value = json.loads(request.body.decode('utf-8'))
    name = value.get('name')
    user_info = User.objects.get(user_name=name)
    data = {
        'code': 0,
        'data': {
            'user_id': user_info.id,
            'user_name': user_info.user_name,
            'email': user_info.email,
            'phone': user_info.phone,
            'project': user_info.project,
            'department': user_info.department,
            'header': user_info.header
        },
        'msg': "请求成功"
    }
    return JsonResponse(data)


@check_login
def update_info(request):
    '''
    更新用户信息
    :param request:
    :return:
    '''
    if request.method == "POST":
        font_user = request.POST
        if font_user.get('user_name') and font_user.get('project'):
            user_id = font_user.get('user_id')
            user_info = User.objects.get(user_id=user_id)
            user_info.user_name = font_user.get('user_name')
            user_info.department = font_user.get('deptname')
            user_info.email = font_user.get('email')
            user_info.phone = font_user.get('phone')
            user_info.project = font_user.get('project')
            user_info.header = font_user.get('header')
            user_info.save()
            data = {
                'code': 0,
                'data': {
                    'user_id': id,
                    'user_name': user_info.user_name,
                    'email': user_info.email,
                    'phone': user_info.phone,
                    'project': user_info.project,
                    'department': user_info.department,
                    'header': user_info.header
                },
                'msg': "请求成功"
            }
            return JsonResponse(data)
        else:
            data = {
                'code': 101,
                'msg': 'user_name and project必填'
            }
            return JsonResponse(data)

    else:
        data = {
            'code': 100,
            'msg': '请求方式错误'
        }
        return JsonResponse(data)


@require_GET
@check_login
def user_pwd(request):
    '''
    获取用户信息
    :param request:
    :return:
    '''
    try:
        name = request.GET.get('name')
        user_info = User.objects.get(user_name=name)
        data = {
            'user_id': user_info.id,
            'user_name': user_info.user_name,
            'email': user_info.email,
            'phone': user_info.phone,
            'project': user_info.project,
            'department': user_info.department,
            'pwd': user_info.password
        }
        json = success(data=data, message='success')
        return json

    except Exception:
        data = {
            'param': request.GET.get('name'),
        }
        return params_error(data=data, message="参数异常",)

@require_POST
@check_login
def save_pwd(request):
    '''
    获取用户信息
    :param request:
    :return:
    '''
    try:
        user_id = request.POST.get('user_id')
        user_info = User.objects.get(user_id=user_id)
        user_info.password = request.POST.get('confirm')
        user_info.save()
        data = {
            'user_id': user_info.id,
            'user_name': user_info.user_name,
            'email': user_info.email,
            'phone': user_info.phone,
            'project': user_info.project,
            'department': user_info.department,
            'pwd': user_info.password
        }
        json = success(data=data, message='success')
        return json

    except Exception:
        data = {
            'param': request.GET.get('name'),
        }
        return params_error(data=data, message="参数异常")


@api_view(['GET'])
@check_login
def get_project(request):
    user_name = request.session.get('name')
    user_id = User.objects.get(user_name=user_name).id
    project_info = Project.objects.filter(user_id=user_id)
    data = {"user_name": user_name,"user_id": user_id, "project_info": project_info}
    return render(request, 'project.html', data)


@api_view(['POST'])
@csrf_exempt
@check_login
def project_list(request):
    '''
    项目列表
    :param request:
    :return:
    '''
    pro_pages = int(request.POST.get('page'))
    project_list = []
    try:
        project_info = Project.objects.all()
        total_num = project_info.count()
        count, remainder = divmod(total_num, 10)

        if remainder == 0:
            sum_page = count
        else:
            sum_page = count + 1

        if project_info:
            for project in project_info:
                project_item = {}
                project_item['id'] = project.id
                project_item['project_name'] = project.project_name
                project_item['user_name'] = User.objects.get(id=project.user_id).user_name
                project_list.append(project_item)
        else:
            project_list = []
    except:
        json = params_error(data={}, message='query data is empty')
        return JsonResponse(json)
    project_list.sort(key=lambda pro_id: pro_id['id'], reverse=True)
    start = (pro_pages - 1) * 10
    end = pro_pages * 10
    project_count = project_list[start:end]
    json = success(data=project_count, message='success', sum_page=sum_page)
    return json


@api_view(['POST'])
@csrf_exempt
@check_login
def add_project(request):
    '''
    添加项目
    :param request:
    :return:
    '''
    project_name = request.POST.get('project_name')
    id = request.POST.get('user_id')
    user_id = User.objects.get(id=id)
    data = {
        'project_name': project_name,
    }
    try:
        Project.objects.create(project_name=project_name, user=user_id)
    except:
        json = params_error(data=data, message='params error')
        return JsonResponse(json)
    json = success(data=data, message='success')
    return json


@api_view(['POST'])
@csrf_exempt
@check_login
def update_project(request):
    '''
    添加项目
    :param request:
    :return:
    '''
    project_name = request.POST.get('project_name')
    id = request.POST.get('project_id')
    data = {
        'project_name': project_name,
        'project_id': id
    }
    try:
        Project.objects.filter(id=id).update(project_name=project_name)
    except Exception as info:
        json = params_error(data=data, message=info)
        return JsonResponse(json)
    json = success(data=data, message='success')
    return json

@api_view(['POST'])
@csrf_exempt
@check_login
def delete_project(request):
    '''
    添加项目
    :param request:
    :return:
    '''
    project_name = request.POST.get('project_name')
    id = request.POST.get('project_id')
    data = {
        'project_name': project_name,
        'project_id': id
    }
    try:
        Project.objects.filter(id=id).delete()
    except Exception as info:
        json = params_error(data=data, message=info)
        return JsonResponse(json)
    json = success(data=data, message='success')
    return json

@api_view(['POST'])
@csrf_exempt
@check_login
def search_project(request):
    '''
    添加项目
    :param request:
    :return:
    '''
    project_name = request.POST.get('project_name')
    create_user = request.POST.get('create_user')
    pro_pages = int(request.POST.get('page'))
    project_list = []
    data = {
        'project_name': project_name,
        'create_user': create_user
    }
    try:
        project_info = Project.objects.filter(project_name__contains=project_name).filter(user__user_name__contains=create_user)
    except Exception as info:
        json = params_error(data=data, message=info)
        return JsonResponse(json)
    total_num = project_info.count()
    count, remainder = divmod(total_num, 10)
    if remainder == 0:
        sum_page = count
    else:
        sum_page = count + 1
    if project_info:
        for project in project_info:
            project_item = {}
            project_item['id'] = project.id
            project_item['project_name'] = project.project_name
            project_item['user_name'] = User.objects.get(id=project.user_id).user_name
            project_list.append(project_item)

    project_list.sort(key=lambda pro_id: pro_id['id'], reverse=True)
    start = (pro_pages - 1) * 10
    end = pro_pages * 10
    project_count = project_list[start:end]
    json = success(data=project_count, message='success', sum_page=sum_page)
    return json

@api_view(['GET'])
@csrf_exempt
@check_login
def get_managecase(request):
    user_name = request.session.get('name')
    user_id = User.objects.get(user_name=user_name).id
    project_info = Project.objects.filter(user_id=user_id)
    data = {"user_name": user_name, "user_id": user_id, "project_info": project_info}
    return render(request, 'managecase.html', data)


@api_view(['POST'])
@csrf_exempt
@check_login
def add_case(request):
    '''
    添加项目
    :param request:
    :return:
    '''

    case_name = request.POST.get('case_name')
    agreement = request.POST.get('agreement')
    route = request.POST.get('route')
    domain_name = request.POST.get('domain_name')
    port = request.POST.get('port')
    method = request.POST.get('method')
    parameter = request.POST.get('parameter')

    data = {
        'case_name': case_name,
        'agreement': agreement,
        'route': route,
        'domain_name': domain_name,
        'port': port,
        'method': method,
        'parameter': parameter,
    }
    try:
        Case.objects.create(case_name=case_name, agreement=agreement, domain_name=domain_name,
                               port=port, method=method, parameter=parameter, route=route)
    except Exception as info:
        json = params_error(data=data, message=info)
        return JsonResponse(json)
    json = success(data=data, message='success')
    return json

@api_view(['POST'])
@csrf_exempt
@check_login
def case_list(request):
    '''
    项目列表
    :param request:
    :return:
    '''
    case_pages = int(request.POST.get('page'))
    case_list = []
    try:
        case_info = Case.objects.all()
        total_num = case_info.count()
        count, remainder = divmod(total_num, 10)

        if remainder == 0:
            sum_page = count
        else:
            sum_page = count + 1

        if case_info:
            for case in case_info:
                case_item = {}
                case_item['id'] = case.id
                case_item['case_name'] = case.case_name
                case_item['agreement'] = case.agreement
                case_item['domain_name'] = case.domain_name
                case_item['route'] = case.route
                case_item['port'] = case.port
                case_item['method'] = case.method
                case_item['parameter'] = case.parameter
                case_list.append(case_item)
        else:
            case_list = []
    except Exception as info:
        json = params_error(data={}, message=info)
        return JsonResponse(json)
    case_list.sort(key=lambda case_id: case_id['id'], reverse=True)
    start = (case_pages - 1) * 10
    end = case_pages * 10
    project_count = case_list[start:end]
    json = success(data=project_count, message='success', sum_page=sum_page)
    return json

@api_view(['POST'])
@csrf_exempt
@check_login
def update_case(request):
    '''
    添加项目
    :param request:
    :return:
    '''
    case_name = request.POST.get('case_name')
    agreement = request.POST.get('agreement')
    route = request.POST.get('route')
    domain_name = request.POST.get('domain_name')
    port = request.POST.get('port')
    method = request.POST.get('method')
    parameter = request.POST.get('parameter')
    case_id = request.POST.get('case_id')
    data = {
        'case_id': case_id,
        'case_name': case_name,
        'agreement': agreement,
        'route': route,
        'domain_name': domain_name,
        'port': port,
        'method': method,
        'parameter': parameter,
    }
    try:
        Case.objects.filter(id=case_id).update(case_name=case_name, agreement=agreement, domain_name=domain_name,
                               port=port, method=method, parameter=parameter, route=route)
    except Exception as info:
        json = params_error(data=data, message=info)
        return JsonResponse(json)
    json = success(data=data, message='success')
    return json

@api_view(['POST'])
@csrf_exempt
@check_login
def delete_case(request):
    '''
    添加项目
    :param request:
    :return:
    '''

    case_id = request.POST.get('case_id')
    data = {
        'case_id': case_id
    }
    try:
        Case.objects.filter(id=case_id).delete()
    except Exception as info:
        json = params_error(data=data, message=info)
        return JsonResponse(json)
    json = success(data=data, message='success')
    return json


@api_view(['POST'])
@csrf_exempt
@check_login
def copy_case(request):
    '''
    添加项目
    :param request:
    :return:
    '''
    try:
        case_id = request.POST.get('case_id')
        case_info = Case.objects.filter(id=case_id)[0]
        case_name = case_info.case_name
        agreement = case_info.agreement
        route = case_info.route
        domain_name = case_info.domain_name
        port = case_info.port
        method = case_info.method
        parameter = case_info.parameter
        print(case_info)
    except Exception as info:
        json = params_error(data=[], message=info)
        return JsonResponse(json)
    data = {
        'case_id': case_id,
        'case_name': case_name,
        'agreement': agreement,
        'route': route,
        'domain_name': domain_name,
        'port': port,
        'method': method,
        'parameter': parameter,
    }
    try:
        Case.objects.create(case_name=case_name, agreement=agreement, domain_name=domain_name,
                            port=port, method=method, parameter=parameter, route=route)
    except Exception as info:
        json = params_error(data=data, message=info)
        return JsonResponse(json)
    json = success(data=data, message='success')
    return json


@api_view(['POST'])
@csrf_exempt
@check_login
def execute_case(request):
    '''
    添加项目
    :param request:
    :return:
    '''
    case_id = request.POST.get('case_id')
    data = {
        'case_id': case_id
    }
    try:
        # case_info = Case.objects.filter(id=case_id)[0]
        result = excuse_case()
    except Exception as info:
        json = params_error(data=data, message=info)
        return JsonResponse(json)
    json = success(data=result, message='success')



    return json