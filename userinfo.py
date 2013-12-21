# -*- coding:utf8 -*-
''' 自訂模組 '''
from dictdb import DictDB

class Userinfo(DictDB):
    ''' 存取使用者資料庫 '''
    def __init__(self, *args, **kwargs):
        super(Userinfo, self).__init__(fname='userinfo.json', *args, **kwargs)
