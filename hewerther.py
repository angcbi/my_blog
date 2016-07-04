#!/home/caicai/.virtualenvs/Dev/bin/python
# encoding: utf-8

import os
import pdb
import cPickle
import requests
import datetime
import traceback



def getCityId(city='北京', key='84b9f014191c4257bb31edd4fa5b1837'):
    dir = os.path.dirname(__name__)
    filename = os.path.join(dir, 'citylist.txt')
    try:
        if not (os.path.exists(filename) and datetime.datetime.fromtimestamp(os.path.getctime(filename)) > datetime.datetime.now() - datetime.timedelta(days=7)):
            print u'未检测到citylist文件或文件过旧，更新文件'
            url = 'https://api.heweather.com/x3/citylist'
            params = {
                'search':'allchina',
                'key': key,
                }
            try:
                r = requests.get(url=url, params=params)
                if r.status_code == requests.codes.ok:
                    data = r.json().get('city_info')
                    print u'本次获取{}条记录，写入文件{}'.format(len(data), filename)
                    file = open(filename, 'wb')
                    cPickle.dump(data, file)
                    file.close()
                    print u'写入完成'
            except requests.exceptions.RequestException, e:
                print e


        with open(filename, 'rb') as f:
            data = cPickle.load(f)

        print u'读取%d条记录' % len(data)
        for item in data:
            if item['city'] == city.decode('utf8'):
                id = item.get('id')
                print u'{}的id为{}'.format(city.decode('utf8'), id)
                return id

        print u'未找到%s的cityid，默认为CN101010100' % city.decode('utf8')
    except Exception, e:
        #print e
        print traceback.format_exc()

    return 'CN101010100'

def parsedata(data):
    HeWeatherdataservice = data.get('HeWeather data service 3.0', [])
    for item in HeWeatherdataservice:
        status = item.get('status')
        if status == 'ok':
            hourly_forecast = item.get('hourly_forecast', {})
            suggestion = item.get('suggestion', {})
            daily_forecast = item.get('daily_forecast', {})
            now = item.get('now', {})
            aqi = item.get('aqi', {})
            alarms = item.get('alarms', {})
            basic = item.get('basic', {})
            daily_forecast = item.get('daily_forecast', {})

            # 空气质量
            aqi1 = aqi.get('city', {}).get('aqi', '')
            pm25 = aqi.get('city', {}).get('pm25', '')
            pm10 = aqi.get('city', {}).get('pm10', '')

            # 实况天气
            tmp = now.get('tmp')
            vis = now.get('vis')
            hum = now.get('hum')
            pcpn_now = now.get('pcpn')
            txt = now.get('cond', {}).get('txt')
            code = now.get('cond', {}).get('code')
            code_url = 'http://files.heweather.com/cond_icon/' + code + '.png'
            sc = now.get('wind', {}).get('sc')

            # 生活指数
            sport_bur = suggestion.get('sport', {}).get('brf')
            sport_txt = suggestion.get('sport', {}).get('txt')
            drsg_bur = suggestion.get('drsg', {}).get('brf')
            drsg_txt = suggestion.get('drsg', {}).get('txt')

            # 基本信息
            city = basic.get('city')
            time = basic.get('update', {}).get('loc')

            # 天气预报

            print u'时间：{}， 城市：{}， 天气：{}， {}，温度：{}℃, 风力{}级'.format(time, city, txt, code_url, tmp, sc)
            print u'空气质量指数:{}, PM2.5:{}, PM10:{}'.format(aqi1, pm25, pm10)
            print u'运动指数：{}，{} \n穿衣指数:{}, {}'.format(sport_bur, sport_txt, drsg_bur, drsg_txt)

            item = daily_forecast[1]
            tmp_max = item.get('tmp', {}).get('max', '')
            tmp_min = item.get('tmp', {}).get('max', '')
            pop = item.get('pop', '')
            popn = item.get('popn', 0)
            txt_d = item.get('cond', {}).get('txt_d', '')
            code_d = item.get('cond', {}).get('code_d', '')
            code_d_url = 'http://files.heweather.com/cond_icon/' + code_d + '.png'
            txt_n = item.get('cond', {}).get('txt_n', '')
            code_n = item.get('cond', {}).get('code_n', '')
            code_n_url = 'http://files.heweather.com/cond_icon/' + code_n + '.png'
            sc = item.get('wind', {}).get('sc', '')
            spd = item.get('wind', {}).get('spd', '')
            date = item.get('date')

    print  u'{}{},天气：{}，温度：{}℃，风力：{}，降雨量：{}mm；明天白天：{}，晚上：{}，气温：{}-{}℃，降水概率：{}%，降水量：{}mm。【天气助手】'.\
        format(time, city, txt, tmp, sc, pcpn_now, txt_d, txt_d, tmp_min, tmp_max, pop, popn)

    return  '{}{},天气：{}，温度：{}℃，风力：{}，降雨量：{}mm；明天白天：{}，晚上：{}，气温：{}-{}℃，降水概率：{}%，降水量：{}mm。【天气助手】'.\
        format(time, city, txt, tmp, sc, pcpn_now, txt_d, txt_d, tmp_min, tmp_max, pop, popn)

def weather(city, key='84b9f014191c4257bb31edd4fa5b1837'):
    cityId = getCityId(city, key)
    params = {
            'cityid': cityId,
            'key': key
        }

    url = 'https://api.heweather.com/x3/weather'
    try:
        r = requests.get(url, params=params)
        content = parsedata(r.json())
        sendSms(content)

    except Exception, e:
        print e


def sendSms(content):
    params = {
        'appkey':'8de49e132e8a53da',
        'mobile':'18500612841',
        'content': content
    }
    url = 'http://api.jisuapi.com/sms/send'
    try:
        r = requests.get(url, params=params)
        if r.status_code == requests.codes.ok:
            if r.json().get('status') == '0':
                print u'发送成功，接收人{}，发送{}条'.format(params['mobile'], r.json().get('result', {}).get('count'))
            else:
                print r.json().get('msg')
    except requests.exceptions.RequestException, e:
        print e




if __name__ == '__main__':
    weather('邓州')
"""
search:
        allchina,国内城市
        hotworld,热门城市
        allworld,全部城市
"""



"""


url = 'https://api.heweather.com/x3/weather?cityid=城市ID&key=你的认证key'


'空气质量指数' aqi.aqi
'pm2.5'        aqi.pm25
'空气质量类别' aqi.qlty


'灾害预警' alarms

标题 title

type 类型
level 级别

txt 描述
stat 状态
"""
