#导包
from captcha.image import ImageCaptcha
from PIL import Image
import random
import time
import jwt
import os
from Share.Route import Any_Path
import os
import django
os.environ['DJANGO_SETTINGS_MODULE']='AutoPlatform.settings'
django.setup()
from Platform.models import VerifiCode
from Platform.models import User

def verify_code(length=4):

    '''
    生成随机4位字符
    :return:
    '''

    number = [str(i) for i in range(10)]            #生成数据列表
    capita = [chr(j) for j in range(65,91)]         #生成大写字母
    letter = [chr(k) for k in range(97, 123)]       #生成小写字母列表
    code_list = number + capita + letter            #由大小写字母数字组合一个列表
    code = ''.join(random.sample(code_list, length))   #将选取元素组合成字符串

    return code


def generate_captcha():
    '''
    生成验证码图片
    :return:
    '''

    image = ImageCaptcha()          #生成验证码对象
    verify = verify_code()          #生成字符串
    VerifiCode.objects.create(code=verify)
    captcha_image = Image.open(image.generate(verify))
    return captcha_image


def save_captcha(path='image', filename='verify.png'):
    '''
    保存图片
    :param path:
    :return:
    '''
    save_path = Any_Path(path)
    image = generate_captcha()
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_path = Any_Path(path, filename)
    image.save(save_path)

    return filename


def token():
    token = jwt.encode({'username': 'admin', 'site': 'https://ops-coffee.cn'}, 'secret_key', algorithm='HS256')
    return token