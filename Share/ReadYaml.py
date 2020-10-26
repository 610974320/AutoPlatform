import yaml
from Share.Route import Any_Path
from Share.FontColor import outcome
import os


class ReadConfig:
    def __init__(self,key=None,configdir='ConfigDir',file='Config.yaml', encoding='utf-8'):
        '''
        读取yaml文件中的内容
        :param key:需要取值的键
        :param dir: 配置文件的目录名称
        :param file: 配置文件的名称
        :param encoding: 编码格式
        '''
        self.key = key
        self.file = file
        self.configdir = configdir
        self.encoding = encoding

    @property
    def config_data(self):
        """读取yaml里所有的内容"""
        self.path = Any_Path(self.configdir, self.file)
        if os.path.exists(self.path):
            f = open(self.path, encoding=self.encoding)
            data = yaml.load(f)
            f.close()
            return data
        else:
            outcome('red', f"请检此路径:{self.path},下的用例文件是否存在")

    @property
    def base_config(self):
        '''
        获取base_config键对应的键值
        :return:
        '''
        if self.key:
            return self.config_data.get('base_config').get(self.key)
        else:
            outcome('red', f"请输入必要的参数,建议请输入【base_config】参数...!")

    @property
    def base_url(self):
        '''
        获取base_url键值
        :return:
        '''
        if self.key:
            return self.config_data.get('base_url').get(self.key)
        else:
            outcome('red', f"请输入必要的参数,建议请输入【base_url】参数...!")

    @property
    def email(self):
        '''
        获取email键值
        :return:
        '''
        if self.key:
            return self.config_data.get('email').get(self.key)
        else:
            outcome('red', f"请输入必要的参数,建议请输入【email】参数...!")

    @property
    def sql(self):
        '''
        获取sql键值
        :return:
        '''
        if self.key:
            return self.config_data.get('sql').get(self.key)
        else:
            outcome('red', f"请输入必要的参数,建议请输入【sql】参数...!")

    @property
    def report(self):
        '''
        获取report键值
        :return:
        '''
        if self.key:
            return self.config_data.get('report').get(self.key)
        else:
            outcome('red', f"请输入必要的参数,建议请输入【report】参数...!")

if __name__ == '__main__':
    data = ReadConfig("pieces_page").base_config
    print(data)
