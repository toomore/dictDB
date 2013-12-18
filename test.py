# -*- coding:utf8 -*-
''' unittest '''
from dictdb import DictDB
from dictdb import getdatetime
import unittest

class Testdd(unittest.TestCase):
    ''' unittest '''

    def test_adddata(self):
        ''' 範例 新增資料 '''
        print '{0:-^30}'.format('do_adddata')
        data = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
        result = DictDB().insert(data) #新增一筆資料
        print result
        data = {'name': 'toomore', 'age': 28}
        result = DictDB().insert(data) #新增一筆資料
        print result

    def test_find(self):
        ''' 範例 取所有資料 '''
        print '{0:-^30}'.format('do_find')
        print list(DictDB().find())

    def test_find_something(self):
        ''' 範例 取所有資料 '''
        print '{0:-^30}'.format('do_find_something')
        print list(DictDB().find({'name':'toomore'}))

    def test_find_one(self):
        ''' 範例 取資料 '''
        print '{0:-^30}'.format('do_find_one')
        print DictDB().find_one({'name':'toomore'})

    def test_update(self):
        ''' 範例 修改資料  '''
        print '{0:-^30}'.format('do_update')
        data = {'name': 'toomore2', 'age': 18} #原資料
        getinsert = DictDB().insert(data) #新增資料
        print getinsert #印出新增資料
        data = {'name': 'toomore_update', 'age':28, 'loc':'kaohsiung'} #欲修改資料內容
        DictDB().update(getinsert, data) #修改資料
        print DictDB().find_one({'_id': getinsert.get('_id')}) #印出修改後的資料

    def test_del(self):
        ''' 範例 刪除資料 '''
        print '{0:-^30}'.format('do_del')
        data = {'name': 'toomore_del', 'age': 18}
        getinsert = DictDB().insert(data) #將新增資料
        print DictDB().find_one({'_id': getinsert.get('_id')}) #印出資料
        DictDB().remove({'_id': getinsert.get('_id')}) #刪除資料
        print DictDB().find_one({'_id': getinsert.get('_id')}) #印出剛刪除的資料 None
        print list(DictDB().find()) #印出所有資料

    def test_getdatetime(self):
        ''' 範例 轉換 _id 為時間值 '''
        print '{0:-^30}'.format('do_getdatetime')
        data = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
        result = DictDB().insert(data) #新增一筆資料
        print result
        print getdatetime(result.get('_id'))

if __name__ == "__main__":
    unittest.main()
