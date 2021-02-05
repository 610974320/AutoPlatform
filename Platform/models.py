from django.db import models
# from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from AutoPlatform import settings
import jwt
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager

# Create your models here.
#python manage.py makemigrations
#python manage.py migrate
#delete from django_migrations;
#python manage.py migrate --fake

import django.utils.timezone as timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token


class VerifiCode(models.Model):
    '''
    验证码表
    '''
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.code


class User(models.Model):
    '''
    用户表
    '''
    user_name = models.CharField(max_length=20, verbose_name='admin', null=False)   #用户名
    password = models.CharField(max_length=50, verbose_name='123456', null=False)    #密码
    phone = models.CharField(max_length=20, null=True)      #电话号码
    email = models.CharField(max_length=50, null=True)       #邮箱
    department = models.CharField(max_length=40, null=True)   #部门
    project_name = models.CharField(max_length=30, verbose_name='营销云', null=False)     #项目
    header = models.TextField(max_length=20000, null=True)    #头像

    def __str__(self):
        return self.user_name


class Project(models.Model):
    '''
    模块表
    '''
    project_name = models.CharField(max_length=20, null=False)              #模块名称
    create_date = models.DateTimeField('创建日期', default=timezone.now)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


    def __str__(self):
        return self.project_name


class Model(models.Model):
    '''
    模块表
    '''
    model_name = models.CharField(max_length=20, null=False)   #模块名称
    create_date = models.DateTimeField('创建日期', default=timezone.now)
    project = models.ForeignKey("Project",  on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name


class Case(models.Model):
    '''
    模块表
    '''
    case_name = models.CharField(max_length=500, null=False)              #模块名称
    agreement = models.CharField(max_length=20)
    domain_name = models.CharField(max_length=300)
    port = models.CharField(max_length=50)
    method = models.CharField(max_length=30)
    route = models.CharField(max_length=5000)
    code = models.CharField(max_length=50)
    parameter = models.TextField(max_length=20000)
    create_date = models.DateTimeField('创建日期', default=timezone.now)

    def __str__(self):
        return self.case_name