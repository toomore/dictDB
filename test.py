#!/usr/bin/env python
# -*- coding:utf8 -*-
import unittest
from dd import dictdata
from dd import getdatetime

class testdd(unittest.TestCase):

    def test_adddata(self):
        ''' 範例 新增資料 '''
        print '{0:-^30}'.format('do_adddata')
        d = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
        a = dictdata().insert(d) #新增一筆資料
        print a
        d = {'name': 'toomore', 'age': 28}
        a = dictdata().insert(d) #新增一筆資料
        print a

    def test_find(self):
        ''' 範例 取所有資料 '''
        print '{0:-^30}'.format('do_find')
        print list(dictdata().find())

    def test_find_something(self):
        ''' 範例 取所有資料 '''
        print '{0:-^30}'.format('do_find_something')
        print list(dictdata().find({'name':'toomore'}))

    def test_find_one(self):
        ''' 範例 取資料 '''
        print '{0:-^30}'.format('do_find_one')
        print dictdata().find_one({'name':'toomore'})

    def test_update(self):
        ''' 範例 修改資料  '''
        print '{0:-^30}'.format('do_update')
        d = {'name': 'toomore2','age': 18} #原資料
        getinsert = dictdata().insert(d) #新增資料
        print getinsert #印出新增資料
        d = {'name': 'toomore_update','age':28,'loc':'kaohsiung'} #欲修改資料內容
        dictdata().update(getinsert, d) #修改資料
        print dictdata().find_one({'_id': getinsert.get('_id')}) #印出修改後的資料

    def test_del(self):
        ''' 範例 刪除資料 '''
        print '{0:-^30}'.format('do_del')
        u = {'name': 'toomore_del','age': 18}
        getinsert = dictdata().insert(u) #將新增資料
        print dictdata().find_one({'_id': getinsert.get('_id')}) #印出資料
        dictdata().remove({'_id': getinsert.get('_id')}) #刪除資料
        print dictdata().find_one({'_id': getinsert.get('_id')}) #印出剛刪除的資料 None
        print list(dictdata().find()) #印出所有資料

    def test_getdatetime(self):
        ''' 範例 轉換 _id 為時間值 '''
        print '{0:-^30}'.format('do_getdatetime')
        d = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
        a = dictdata().insert(d) #新增一筆資料
        print a
        print getdatetime(a.get('_id'))

if __name__ == "__main__":
    unittest.main()
