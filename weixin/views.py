#!/usr/bin/env python
# encoding:utf-8

import socket
from django.shortcuts import render
from django.http import HttpResponse
from utils import check_Signature

def checkSignature(request):
    print request.method
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')
    print socket.gethostname()

    if check_Signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponse(echostr)

    return HttpResponse('')

