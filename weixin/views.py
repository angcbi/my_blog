import hashlib
from django.shortcuts import render
from django.http improt HttpResponse
from utils import checkSignature

def checkSignature(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')

    if checkSignature(signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponse(echostr)

    return HttpResponse('')

