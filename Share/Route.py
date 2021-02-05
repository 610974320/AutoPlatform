import os


def Any_Path(*args):
    '''
    获取任何目录
    :param args: 逐级目录名称
    :return:  返回给定目录路径
    '''
    any_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), *args)
    return any_path

