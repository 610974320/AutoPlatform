import sys

def coloring():
    """输出终端时给字体着色
       显示格式: \033[显示方式;前景色;背景色m
       只写一个字段表示前景色,背景色默认
    """
    color_dict = {
        'red': '\033[31m',  # 红色
        'green': '\033[32m',  # 绿色
        'yellow': '\033[33m',  # 黄色
        'blue': '\033[34m',  # 蓝色
        'fuchsia': '\033[35m', # 紫红色
        'cyan': '\033[36m',  # 青蓝色
        'white': '\033[37m',  # 白色
        'reset': '\033[0m',  # 终端默认颜色
    }
    return color_dict


def outcome(color,param,end="\n"):
    '''
    :param color:
    :param param:
    :param end:
    :return:
    '''
    param = str(param)
    return sys.stdout.write(coloring()[color] + param + end)

