#!/usr/bin/env python
# encoding:utf-8

import json
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils import check_Signature, parseXml
#from utils import check_Signature, parseXml, tuling

@csrf_exempt
def checkSignature(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')

        if check_Signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponse(echostr)
    
    if request.method == 'POST':
        result = ''
        xml = request.body
        data = parseXml(xml) 

        FromUserName = data.get('FromUserName')
        ToUserName = data.get('ToUserName')
        MsgType = data.get('MsgType')
        CreateTime = data.get('CreateTime')
        MsgId = data.get('MsgId')

        if MsgType == 'text':
            result = data.get('Content')
            #content, url = tuling(result, MsgId)
            ret = {
                    'fromusername': ToUserName,
                    'tousername': FromUserName,
                    'createtime': int(time.time()),
                    'content': result 
                    #'content': content + url
                    }
            return render(request, 'reply_text.xml', ret)
        elif MsgType == 'voice':
            pass
        elif MsgType == 'video':
            pass
        elif MsgType == 'shortvide':
            pass
        elif MsgType == 'location':
            pass
        elif MsgType == 'link':
            pass
        else:
            pass
        return HttpResponse(data)

    return HttpResponse('OK')
