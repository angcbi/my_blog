#!/usr/bin/env python
# encoding: utf-8

'''
    from models import article前，需要进行两步，否则报错
    1，指定DJANGO_SETTING_MODULE 环境变量
    2，导入django，执行django.setup()
'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")

import time
from random import randint
from my_blog import settings
from article.models import Article as ar


import django
django.setup()

for i in range(10):
    sl = randint(5, 15)
    ar.objects.create(title = 'Hello,' + str(sl), category = 'Python', content =  u'哈哈')
    time.sleep(sl)
