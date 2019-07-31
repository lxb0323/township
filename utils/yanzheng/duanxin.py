from django.core.cache import cache

import urllib.request
import urllib.error
import xml.dom.minidom

import hashlib
import requests
import json
from urllib.parse import quote


def smsseng(mobile,msg,code):
    url = "http://cf.51welink.com/submitdata/Service.asmx/g_Submit"
    ontent = "'尊敬的用户您好，您的{}验证码为{}，三分钟内有效！'".format(msg,code)
    print(ontent)

    #定义需要进行发送的数据
    param = {'sname':'dlcdwyl0',        #账号
            'spwd':'xintiao123',          #密码  
            'scorpid':'',           #企业代码
            'sprdid':'1012818',     #产品编号
            'sdst':mobile,   #手机号码
            'smsg':ontent}       #短信内容
    data = urllib.parse.urlencode(param).encode(encoding='UTF8')
    # print(data)
    #定义头
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    #开始提交数据
    req = urllib.request.Request(url, data, headers)   
    response = urllib.request.urlopen(req)
    #获取返回数据
    result = response.read().decode('utf8')
    print(result)

    #自行解析返回结果xml，对应结果参考文档
    dom = xml.dom.minidom.parseString(result)
    root = dom.documentElement
    State = root.getElementsByTagName("State")
    MsgID = root.getElementsByTagName("MsgID")
    MsgState = root.getElementsByTagName("MsgState")
    Reserve = root.getElementsByTagName("Reserve")
    data = {'result':State[0].firstChild.data,'msg_id':MsgID[0].firstChild.data,
          'msg_state':MsgState[0].firstChild.data,'reserve':Reserve[0].firstChild.data}
    # print(State[0].firstChild.data)  #State值为0表示提交成功
    # print(MsgID[0].firstChild.data)
    # print(MsgState[0].firstChild.data)
    # print(Reserve[0].firstChild.data)
    return data


def encryption_md5(data):
    '''
        排序，加密
    '''
    # key = 'dcbe1dc651e44ac0838dfb725a5e645d'
    # print(data.items())
    adata = sorted(data.items(),key= lambda x:str(x[0][0]))
    print(adata,'-----------------------------')
    new_d = '&'.join('{}={}'.format(k,v) for k,v in adata) + "&key=I6wfoo"
    print(new_d)
    return hashlib.md5(new_d.encode('utf-8')).hexdigest().upper()

def zhankui_smsseng(mobile,msg,code):
    content = "'尊敬的用户您好，您的{}验证码为{}，三分钟内有效！'".format(msg,code)
    data = {
            'account': 'cdyfyjr-HY',
            'phones': str(mobile),
            'content': content,
        }
    data["sign"] = encryption_md5(data)
    # return data
    mepost=requests.post("http://39.104.191.22:8082/sms/api/send/message",json=data)
    return json.loads(mepost.content)



def verify_sms(timestamp_key=None, captcha=None):
    captcha = int(captcha)
    if cache.get(timestamp_key) is None:
        return 1
    if timestamp_key and captcha and captcha == cache.get(timestamp_key):
        if cache.get(timestamp_key) is None:
            return 0
        cache.delete(timestamp_key)
        return 4
    elif timestamp_key and captcha and captcha != cache.get(timestamp_key):
        if cache.get(timestamp_key) is None:
            return 1
        print(type(captcha),555555555555555555555555555)
        print(type(cache.get(timestamp_key)),2222222222222222)
        return 2
    else:
        return 3