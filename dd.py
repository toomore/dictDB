#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
import os
from datetime import datetime
from time import mktime

def getunitime():
    ''' 取得一個微時間值 '''
    t = datetime.utcnow()
    return '{0}{1:06}'.format(int(mktime(t.timetuple())), t.microsecond)

def getdatetime(t):
    ''' 將 _id 轉回時間值 '''
    return datetime.fromtimestamp(int(t)/1000000.0)

class dictdata(object):
    ''' 資料庫存取基本功能 '''
    def __init__(self, unikey=0, fname='./test.json'):
        ''' 確認檔案是否存在，否則建立一個內容為 {} 的檔案
            :no: 資料代碼
            :fname: 檔案位置
        '''
        self.files = fname
        try:
            with open(self.files) as f: pass
        except:
            file(self.files,'w+').write(json.dumps({}))
        self.data = json.loads(file(self.files, 'r+').read())
        #self.unikey = getunitime() if unikey == 0 else unikey

    def save(self):
        ''' 將目前的資料寫入檔案 '''
        file(self.files,'w+').write(json.dumps(self.data))
        self.backup()

    def backup(self):
        ''' 備份檔案 '''
        os.makedirs('./backup') if not os.path.exists('./backup') else None
        d = datetime.strftime(datetime.utcnow(),'%Y%m%d%H%M%S_%f')
        file('./backup/{0}.{1}'.format(self.files, d),'w+').write(json.dumps(self.data))

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
            for d in self.find(i):
                self.data[d.get('_id')].update(toupdate)
        else:
            getdata = self.find_one(i)
            self.data[getdata.get('_id')].update(toupdate)
        self.save()

    def find(self, tofind={}, reverse=True, style="AND"):
        ''' 尋找資料
            :tofind: 欲尋找的資料
        '''
        assert isinstance(tofind, dict)
        def indict(a,b):
            ''' 嚴格符合 '''
            return all([0 if i not in b else 1 if a.get(i) == b.get(i) else 0 for i in a])
        def ORindict(a,b):
            ''' 模糊符合 '''
            return any([0 if i not in b else 1 if a.get(i) in b.get(i) else 0 for i in a])
        ckstyle = indict if style == "AND" else ORindict
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
        assert isinstance(todel ,dict)
        for i in [ i.get('_id') for i in self.find(todel)]:
            del self.data[i]
        self.save()

#---------- 自訂模組 -----------#
class userinfo(dictdata):
    ''' 存取使用者資料庫 '''
    def __init__(self, *arg):
        dictdata.__init__(self, *arg, fname='./userinfo.json')

#---------- 範例 -----------#
def do_adddata():
    ''' 範例 新增資料 '''
    d = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
    a = dictdata().insert(d) #新增一筆資料
    print a
    d = {'name': 'toomore', 'age': 28}
    a = dictdata().insert(d) #新增一筆資料
    print a

def do_find():
    ''' 範例 取所有資料 '''
    print list(dictdata().find())

def do_find_something():
    ''' 範例 取所有資料 '''
    print list(dictdata().find({'name':'toomore'}))

def do_find_one():
    ''' 範例 取資料 '''
    print dictdata().find_one({'name':'toomore'})

def do_update():
    ''' 範例 修改資料  '''
    d = {'name': 'toomore2','age': 18} #原資料
    getinsert = dictdata().insert(d) #新增資料
    print getinsert #印出新增資料
    d = {'name': 'toomore_update','age':28,'loc':'kaohsiung'} #欲修改資料內容
    dictdata().update(getinsert, d) #修改資料
    print dictdata().find_one({'_id': getinsert.get('_id')}) #印出修改後的資料

def do_del():
    ''' 範例 刪除資料 '''
    u = {'name': 'toomore_del','age': 18}
    getinsert = dictdata().insert(u) #將新增資料
    print dictdata().find_one({'_id': getinsert.get('_id')}) #印出資料
    dictdata().remove({'_id': getinsert.get('_id')}) #刪除資料
    print dictdata().find_one({'_id': getinsert.get('_id')}) #印出剛刪除的資料 None
    print list(dictdata().find()) #印出所有資料

def do_getdatetime():
    ''' 範例 轉換 _id 為時間值 '''
    d = {'name': 'eromoot', 'age': 28, 'info': u'中文…'}
    a = dictdata().insert(d) #新增一筆資料
    print a
    print getdatetime(a.get('_id'))

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
