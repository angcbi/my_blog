#!/usr/bin/env python
# encoding: utf-8


def checkSignature(signature, timestamp, nonce):

    token = 'caicai'

    L = [timestamp, nonce, token]
    L.sort()

    code = reduce(lambda x,y : str(x)+str(y), L)
    hashcode = hashlib.md5(code).hexdigest

    if hashcode == signature:
        return True
    return False

