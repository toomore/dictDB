# -*- coding:utf8 -*-
''' Python dict database '''
from datetime import datetime
from time import mktime
import json
import os
import zlib

def getunitime():
    ''' 取得一個微時間值 '''
    now = datetime.utcnow()
    return '{0}{1:06}'.format(int(mktime(now.timetuple())), now.microsecond)

def getdatetime(timestamp):
    ''' 將 _id 轉回時間值 '''
    return datetime.fromtimestamp(int(timestamp)/1000000.0)

class DictDB(object):
    ''' 資料庫存取基本功能 '''
    def __init__(self, fname='test.json', backupdirname='backup'):
        ''' 確認檔案是否存在，否則建立一個內容為 {} 的檔案
            :no: 資料代碼
            :fname: 檔案位置
        '''
        self.fname = fname
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.files = os.path.join(self.dirname, fname)
        self.backupfilepath = os.path.join(self.dirname, backupdirname)

        if not os.path.exists(self.files):
            with file(self.files, 'w+') as file_data:
                file_data.write(zlib.compress(json.dumps({}), 9))

        if not os.path.exists(self.backupfilepath):
            os.makedirs(self.backupfilepath)

        with file(self.files, 'r+') as files:
            self.data = json.loads(zlib.decompress(files.read()))

    def save(self):
        ''' 將目前的資料寫入檔案 '''
        with file(self.files,'w+') as files:
            files.write(zlib.compress(json.dumps(self.data), 9))
            self.backup()

    def backup(self):
        ''' 備份檔案 '''
        file_name = datetime.strftime(datetime.utcnow(),'%Y%m%d%H%M%S_%f')
        with file(os.path.join(self.backupfilepath, '%s.%s' % (self.fname, file_name)), 'w+') as files:
            files.write(zlib.compress(json.dumps(self.data), 9))

    def insert(self, i):
        ''' 建立資料
            :i: 該筆相符資料
        '''
        assert isinstance(i, dict)
        unikey = getunitime()
        i.update({'_id': unikey})
        self.data[str(unikey)] = i
        self.save()
        return i

    def update(self, i, toupdate, more=0):
        ''' 更新資料
            :i: 該筆相符資料
            :toupdate: 欲新增的資料
            :more: 更新所有相符的資料，預設為一筆
        '''
        assert isinstance(i, dict)
        assert isinstance(toupdate, dict)
        if more:
            for data in self.find(i):
                self.data[data.get('_id')].update(toupdate)
        else:
            getdata = self.find_one(i)
            self.data[getdata.get('_id')].update(toupdate)
        self.save()

    def find(self, tofind=None, reverse=True, style="AND"):
        ''' 尋找資料
            :tofind: 欲尋找的資料
        '''
        if tofind:
            assert isinstance(tofind, dict)
        else:
            tofind = {}

        def all_in_dict(tofind, data):
            ''' 嚴格符合 '''
            return all([0 if i not in data else 1 if tofind.get(i) == data.get(i) else 0 for i in tofind])
        def or_in_dict(tofind, data):
            ''' 模糊符合 '''
            return any([0 if i not in data else 1 if tofind.get(i) in data.get(i) else 0 for i in tofind])
        ckstyle = all_in_dict if style == "AND" else or_in_dict
        for i in sorted(self.data, reverse=reverse):
            if ckstyle(tofind, self.data.get(i)):
                yield self.data.get(i)

    def find_one(self, tofind):
        ''' 尋找資料，無資料回傳 None
            :tofind: 欲尋找的資料
        '''
        assert isinstance(tofind, dict)
        getfind = [i.get('_id') for i in list(self.find(tofind))]
        if getfind:
            last = max(getfind)
            return self.data.get(last)
        else:
            return None

    def remove(self, todel):
        ''' 刪除資料
            :todel: 欲刪除的資料
        '''
        assert isinstance(todel, dict)
        for i in [ i.get('_id') for i in self.find(todel)]:
            del self.data[i]
        self.save()

#---------- 自訂模組 -----------#
class Userinfo(DictDB):
    ''' 存取使用者資料庫 '''
    def __init__(self, *args, **kwargs):
        super(Userinfo, self).__init__(fname='userinfo.json', *args, **kwargs)

#---------- 範例 -----------#
def do_adddata():
    ''' 範例 新增資料 '''
    data = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
    result = DictDB().insert(data) #新增一筆資料
    print result
    data = {'name': 'toomore', 'age': 28}
    result = DictDB().insert(data) #新增一筆資料
    print result

def do_find():
    ''' 範例 取所有資料 '''
    print list(DictDB().find())

def do_find_something():
    ''' 範例 取所有資料 '''
    print list(DictDB().find({'name':'toomore'}))

def do_find_one():
    ''' 範例 取資料 '''
    print DictDB().find_one({'name':'toomore'})

def do_update():
    ''' 範例 修改資料  '''
    data = {'name': 'toomore2', 'age': 18} #原資料
    getinsert = DictDB().insert(data) #新增資料
    print getinsert #印出新增資料
    data = {'name': 'toomore_update', 'age':28, 'loc':'kaohsiung'} #欲修改資料內容
    DictDB().update(getinsert, data) #修改資料
    print DictDB().find_one({'_id': getinsert.get('_id')}) #印出修改後的資料

def do_del():
    ''' 範例 刪除資料 '''
    data = {'name': 'toomore_del', 'age': 18}
    getinsert = DictDB().insert(data) #將新增資料
    print DictDB().find_one({'_id': getinsert.get('_id')}) #印出資料
    DictDB().remove({'_id': getinsert.get('_id')}) #刪除資料
    print DictDB().find_one({'_id': getinsert.get('_id')}) #印出剛刪除的資料 None
    print list(DictDB().find()) #印出所有資料

def do_getdatetime():
    ''' 範例 轉換 _id 為時間值 '''
    data = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
    result = DictDB().insert(data) #新增一筆資料
    print result
    print getdatetime(result.get('_id'))

#---------- 執行範例 -----------#
if __name__ == '__main__':
    print '{0:-^30}'.format('do_adddata')
    do_adddata()
    print '{0:-^30}'.format('do_find')
    do_find()
    print '{0:-^30}'.format('do_find_something')
    do_find_something()
    print '{0:-^30}'.format('do_find_one')
    do_find_one()
    print '{0:-^30}'.format('do_update')
    do_update()
    print '{0:-^30}'.format('do_del')
    do_del()
    print '{0:-^30}'.format('do_getdatetime')
    do_getdatetime()