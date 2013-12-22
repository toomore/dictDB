# -*- coding:utf8 -*-
''' unittest '''
from dictdb import DictDB
import unittest

class Testdd(unittest.TestCase):
    ''' unittest '''

    def setUp(self):
        ''' 初始設定  '''
        all_data = DictDB().find()
        for i in all_data:
            DictDB().remove(i)

    def test_adddata(self):
        ''' 測試 新增資料 '''
        print '{0:-^30}'.format('do_adddata')
        data = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
        result = DictDB().insert(data) #新增一筆資料
        print result
        assert data == result
        data = {'name': 'toomore', 'age': 28}
        result = DictDB().insert(data) #新增一筆資料
        print result
        assert data == result

    def test_find(self):
        ''' 測試 取所有資料 '''
        print '{0:-^30}'.format('do_find')
        data = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
        DictDB().insert(data) #新增一筆資料
        result = list(DictDB().find())
        print result
        assert len(list(result)) == 1

    def test_find_something(self):
        ''' 測試 取所有資料 '''
        data = {'name': 'toomore', 'age': 28}
        DictDB().insert(data) #新增一筆資料
        print '{0:-^30}'.format('do_find_something')
        result = list(DictDB().find({'name':'toomore'}))
        print result
        assert len(result) == 1

    def test_find_one(self):
        '''測試 取資料 '''
        data = {'name': 'toomore', 'age': 28}
        DictDB().insert(data) #新增一筆資料
        print '{0:-^30}'.format('do_find_one')
        result = DictDB().find_one({'name':'toomore'})
        print result
        assert result == data

    def test_update(self):
        ''' 測試 修改資料  '''
        print '{0:-^30}'.format('do_update')
        data = {'name': 'toomore2', 'age': 18} #原資料
        getinsert = DictDB().insert(data) #新增資料
        print getinsert #印出新增資料
        data = {'name': 'toomore_update', 'age':28, 'loc':'kaohsiung'} #欲修改資料內容
        DictDB().update(getinsert, data) #修改資料
        result = DictDB().find_one({'_id': getinsert.get('_id')}) #印出修改後的資料
        assert result['age'] == data['age']

    def test_del(self):
        ''' 測試 刪除資料 '''
        print '{0:-^30}'.format('do_del')
        data = {'name': 'toomore_del', 'age': 18}
        getinsert = DictDB().insert(data) #將新增資料
        print DictDB().find_one({'_id': getinsert.get('_id')}) #印出資料
        DictDB().remove({'_id': getinsert.get('_id')}) #刪除資料
        result = DictDB().find_one({'_id': getinsert.get('_id')}) #印出剛刪除的資料 None
        assert result is None

    def test_getdatetime(self):
        ''' 測試 轉換 _id 為時間值 '''
        print '{0:-^30}'.format('do_getdatetime')
        data = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
        result = DictDB().insert(data) #新增一筆資料
        print result
        print DictDB.getdatetime(result.get('_id'))

    def test_clean(self):
        ''' 測試 清空資料 '''
        data = DictDB()
        data.insert({'name': 'toomore'})
        data.clean()
        assert len(list(data.find())) == 1
        data.clean(confirm=True)
        assert len(list(data.find())) == 0


if __name__ == "__main__":
    unittest.main()
