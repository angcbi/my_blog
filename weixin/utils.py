#!/usr/bin/env python
# encoding: utf-8

import requests
import time
import hashlib
import traceback
import xml.etree.cElementTree as et

def check_Signature(signature, timestamp, nonce):

    token = 'caicai'

    L = [timestamp, nonce, token]
    L.sort()

    code = reduce(lambda x,y : str(x)+str(y), L)
    hashcode = hashlib.md5(code).hexdigest

    if hashcode == signature:
        return True
    return False

def getToken():
    data = {
            'grant_type': 'client_credential',
            'appid': 'wx232f6c69fd6779c4',
            'secret': 'f19d95d703e203a66c404c504485e1af',
            }
    tokenurl = 'https://api.weixin.qq.com/cgi-bin/token'

    access_token = ''
    try:
        while True:
            r = requests.get(tokenurl, params=data)
            if r.status_code == requests.codes.ok:
                if r.json().get('errcode'):
                    print r.json().get('errcode'), r.json().get('errmsg')
                access_token = r.json().get('access_token')
                expires_in = r.json().get('expires_in', 7200)
                return  access_token
                time.sleep(expires_in - 60*5)
            else:
                getToken()
    except:
        print traceback.format_exc()

    return None


def parseXml(data):
    ret = {}
    try:
        tree = et.ElementTree(et.fromstring(data))
        for item in tree.iter():
            ret[item.tag] = item.text
    except:
        print traceback.format_exc()

    return ret



if __name__ == '__main__':
    getToken()
