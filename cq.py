#该版本支持手机号匹配快递单号，去掉cmd输出内容，客户详细增加地址
#v1.7 支持查看今日单量，提高批量查询速度，开始使用github
import datetime
import sys
from itertools import chain

from flask import Flask,request
from json import loads
import time
import requests
from http import cookiejar
import urllib.request
import urllib.request
import urllib.parse
# cookiejar用来保存cookie
import http.cookiejar
bot_server = Flask(__name__)


@bot_server.route('/api/message',methods=['POST'])
#路径是你在酷Q配置文件里自定义的
def server():
    data = request.get_data().decode('utf-8')
    data = loads(data)
    messge=data['raw_message']
    long = len(messge)

    if long==11:
        #print(messge)
        yddcx(messge)
        return ''
    elif long==5:
        ydddl()

    elif long==15:
        #print('express')
        yto(messge)


    elif long>21:
        get_cookie()#每次调用get_cookie函数获取cookie
        l = list(map(int, messge.split()))
        #print("input:"+l)
        kd= []
        for t in l:
            kd.append(yddplcx(t))

        bb = "\n".join(kd)
        send(bb)



    else:print('无效查询')
def send(a2):
        #print(a2)
        data = {
            'group_id': 572193706,
            'message': a2,
            'auto_escape': False
        }

        api_url = 'http://127.0.0.1:5700/send_group_msg'
        r = requests.post(api_url, data=data)
        #print(r.text)
def yto(messge):
    url='http://www.yto.net.cn/api/trace/waybill'
    data = {
        'waybillNo': messge
    }
    r=requests.post(url,data=data)
    rj=r.json()
    ifjs=rj['data'][0]['traces']
    if ifjs==None:
        #print(messge,'无走件记录')
        a=messge+'无走件记录'
        send(a)


    else :
        result0 = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(ifjs[0]['time']/1000))))+ifjs[0]['info']
        result1 = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(ifjs[1]['time']/1000))))+ifjs[1]['info']
        #print(messge,result0,',',result1)
        a=messge+'\n'+'最新：'+result0+'\n'+'上一条: '+result1+'\n'
        send(a)

def yddcx(messge):

    cj = http.cookiejar.CookieJar()
    # 创建一个haddler对象
    haddler = urllib.request.HTTPCookieProcessor(cj)
    # 创建一个opener对象
    opener = urllib.request.build_opener(haddler)
    formData = {
        'loginMethod': 'generalLogin',
        'deviceId': 'G4JHX6KI62LPYHWNR2OPCKX3WIBOIGU75DFFHKK6RS5QQDVF75LB4UESP5LLFN57KNYBI6Y2X3QSI3AP5KRYSMMPUY',
        'username': '13827471947',
        'password': 'QH457110'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'cookie': ''
    }
    url = "https://www.1dadan.com/security/loginMain"

    session = requests.Session()

    cookie_jar = session.post(url, formData).cookies

    cookie = requests.utils.dict_from_cookiejar(cookie_jar)
    ecs_t = cookie['ecs_t']











    url = 'https://www.1dadan.com/api/order/list'
    data = {
    'ordersTimeType': 0,
    'startdate': datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month-1,datetime.datetime.now().day),
    'enddate': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
    'shopId': 'all',
    'tradeStatus': 'all',
    'province': 'all',
    'sellerRemarkOrMarkLevel': 'all',
    'serviceType': 'all',
    'refundStatus': 'all',
    'searchKey': 18,
    'searchValue': messge,
    'pageNo': 1,
    'needRefresh': 1,
    'isGroupDisplay': 1,
    'isSingles': 'false',
    'sfPriceMarkupStr': 'all'
    }

    header = {
        'cookie':'_ati=2582860471517; 3AB9D23F7A4B3C9B=G4JHX6KI62LPYHWNR2OPCKX3WIBOIGU75DFFHKK6RS5QQDVF75LB4UESP5LLFN57KNYBI6Y2X3QSI3AP5KRYSMMPUY; fsno=15218833698548; _pati=a2b71ef462b5771fe5d9f95ab9dc42b8; fslb=s1b13; ecs_t=%s'%(ecs_t),
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    r = requests.post(url, data=data,headers=header)
    rj = r.json()


    ifresult1=rj['data']['page']['data']

    if ifresult1==[]:
        a2=messge+'最近一个月没有查询结果'
        send(a2)
    else:
        a3=messge+'总单数：'+str(rj['data']['page']['totalRecord'])
        result1 = rj['data']['page']['data'][0]['data']
        for b in result1:
            ajjr='寄件人：'+b['shipperName']
            a4='姓名电话: '+b['receiverName']+str(b['receiverMobile'])
            a44='详细地址：'+b['receiverFullAddress']
            a5='打印时间：'+time.strftime("%Y-%m-%d %H:%M:%S", (time.localtime(float(b['printDate']/1000))))
            a6='快递单号：'+b['logisticsNo']
            a16=b['logisticsNo']
            a7='订单编号：'+b['trades'][0]['tradeNo']
            a8='产品：'
            list = []
            for c in b['goods']:
                a9=str(c['quantity'])+'件 '+c['goodsName']
                list.append(a9)


            send(a3+'\n'+ajjr+'\n'+a4+'\n'+a44+'\n'+a5+'\n'+a6+'\n'+a7+'\n'+a8+'\n'+str(list)+'\n')

            yto(a16)



#查看易打单今天有多少单
def ydddl():#这个是查询今天有多少单

    cj = http.cookiejar.CookieJar()
    # 创建一个haddler对象
    haddler = urllib.request.HTTPCookieProcessor(cj)
    # 创建一个opener对象
    opener = urllib.request.build_opener(haddler)
    formData = {
        'loginMethod': 'generalLogin',
        'deviceId': 'G4JHX6KI62LPYHWNR2OPCKX3WIBOIGU75DFFHKK6RS5QQDVF75LB4UESP5LLFN57KNYBI6Y2X3QSI3AP5KRYSMMPUY',
        'username': '13827471947',
        'password': 'QH457110'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'cookie': ''
    }
    url = "https://www.1dadan.com/security/loginMain"

    session = requests.Session()

    cookie_jar = session.post(url, formData).cookies

    cookie = requests.utils.dict_from_cookiejar(cookie_jar)
    ecs_t = cookie['ecs_t']
    url = 'https://www.1dadan.com/api/order/list'
    data = {
        'ordersTimeType': 0,
        'startdate': datetime.datetime.now().strftime('%Y-%m-%d')+' 00:00:00',
        'enddate': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
        'shopId': 'all',
        'tradeStatus': 'all',
        'province': 'all',
        'sellerRemarkOrMarkLevel': 'all',
        'serviceType': 'all',
        'refundStatus': 'all',
        'pageNo': 1,
        'needRefresh': 1,
        'isGroupDisplay': 1,
        'isSingles': 'false',
        'sfPriceMarkupStr': 'all'
    }

    header = {
        'cookie':'_ati=2582860471517; 3AB9D23F7A4B3C9B=G4JHX6KI62LPYHWNR2OPCKX3WIBOIGU75DFFHKK6RS5QQDVF75LB4UESP5LLFN57KNYBI6Y2X3QSI3AP5KRYSMMPUY; fsno=15218833698548; _pati=a2b71ef462b5771fe5d9f95ab9dc42b8; fslb=s1b13; ecs_t=%s'%(ecs_t),
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    r = requests.post(url, data=data,headers=header)
    rj = r.json()

    dl=rj['data']['page']['totalRecord']
    s=time.strftime('%Y-%m-%d',time.localtime(time.time()))+' 打单数为：'+str(dl)+'单'

    send(s)




def get_cookie():
    global cok
    cj = http.cookiejar.CookieJar()
    # 创建一个haddler对象
    haddler = urllib.request.HTTPCookieProcessor(cj)
    # 创建一个opener对象
    opener = urllib.request.build_opener(haddler)
    formData = {
        'loginMethod': 'generalLogin',
        'deviceId': 'G4JHX6KI62LPYHWNR2OPCKX3WIBOIGU75DFFHKK6RS5QQDVF75LB4UESP5LLFN57KNYBI6Y2X3QSI3AP5KRYSMMPUY',
        'username': '13827471947',
        'password': 'QH457110'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'cookie': ''
    }
    url = "https://www.1dadan.com/security/loginMain"

    session = requests.Session()

    cookie_jar = session.post(url, formData).cookies

    cookie = requests.utils.dict_from_cookiejar(cookie_jar)
    cok = cookie['ecs_t']
    return cok

def yddplcx(p):
    url = 'https://www.1dadan.com/api/order/list'
    data = {
        'ordersTimeType': 0,
        'startdate': datetime.datetime.now().strftime('%Y-%m-%d')+' 00:00:00',
        'enddate': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        'shopId': 'all',
        'tradeStatus': 'all',
        'province': 'all',
        'sellerRemarkOrMarkLevel': 'all',
        'serviceType': 'all',
        'refundStatus': 'all',
        'searchKey': 18,
        'searchValue': p,
        'pageNo': 1,
        'needRefresh': 1,
        'isGroupDisplay': 1,
        'isSingles': 'false',
        'sfPriceMarkupStr': 'all'
    }

    header = {
        'cookie': '_ati=2582860471517; 3AB9D23F7A4B3C9B=G4JHX6KI62LPYHWNR2OPCKX3WIBOIGU75DFFHKK6RS5QQDVF75LB4UESP5LLFN57KNYBI6Y2X3QSI3AP5KRYSMMPUY; fsno=15218833698548; _pati=a2b71ef462b5771fe5d9f95ab9dc42b8; fslb=s1b13; ecs_t=%s' % (
            cok),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    r = requests.post(url, data=data, headers=header)
    rj = r.json()

    ifresult1 = rj['data']['page']['totalRecord']
    a = []

    if ifresult1 == 0:
        #print("none")
        a.append("none")
    else:
        result1 = rj['data']['page']['data'][0]['data'][0]['logisticsNo']
        #print(result1)
        a.append(result1)

    b=",".join(a)
    return b




#易打单批量查询












if __name__ == '__main__':
    bot_server.run(port=5701)
    #端口也是你在酷Q配置文件里自定义的