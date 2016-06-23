#!/usr/bin/env python
# encoding: utf-8

import requests
import time
import hashlib
import traceback
import json
import xml.etree.cElementTree as et

def check_Signature(signature, timestamp, nonce):

    token = 'caicai'

    L = [timestamp, nonce, token]
    L.sort()

    sha1 = hashlib.sha1()
    map(sha1.update, L)
    hashcode =sha1.hexdigest()

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

def tuling(content, userid=None, location=u'beijing'):
    text, url = '', ''
    url = 'http://www.tuling123.com/openapi/api'
    data = {
            'key': 'e092df54d2067d1c9fe5d317138c0385',
            'info': content,
            'loc': location,
            'userid': userid
            }
    r = requests.get(url, params=data)
    print r.content
    code = r.json().get('code')
    text = r.json().get('text')

    if code == '200000':
        url = r.json().get('url')

    return text, url


if __name__ == '__main__':
    getToken()
