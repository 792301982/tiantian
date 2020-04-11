import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import js2py
import time,sys

def Beijing_time():
    r=requests.get('https://www.baidu.com')
    t=time.strptime(r.headers['date'],'%a, %d %b %Y %H:%M:%S GMT')
    return time.mktime(t)+28800
# if(Beijing_time()>1586494359.015696+86400):
#     input("测试期已过，请联系作者。")
#     sys.exit()

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",

}
islogin_url = "https://pai.ttpai.cn/dealer/isLogin"
# POST

chujia_url = "https://pai.ttpai.cn/bid/newbid"
# GET
# price=100
# auctionId=44884443

login_url = "https://pai.ttpai.cn/dealer/login"
# POST
# mobilePhone: 18623002291
# pswd: a123123
# imageCode:

cars_url = "https://pai.ttpai.cn/"
# POST
# status: 1
# brand:
# cityValues:
# registerValues:
# yearsValues:
# clickCount: 0
# orderUp: asc
# orderBy:
# currentPage: 1

js = '''
function j() {
        date=new Date;
        newGUID = function () {
            date = new Date;
            var i = "";
            sexadecimalDate = hexadecimal(getGUIDDate(), 16),
                sexadecimalTime = hexadecimal(getGUIDTime(), 16);
            for (var e = 0; 9 > e; e++)
                i += Math.floor(16 * Math.random()).toString(16);
            for (i += sexadecimalDate,
                i += sexadecimalTime; i.length < 32;)
                i += Math.floor(16 * Math.random()).toString(16);
            return formatGUID(i)
        }
            
            getGUIDDate = function () {
                return this.date.getFullYear() + this.addZero(this.date.getMonth() + 1) + this.addZero(this.date.getDay())
            }
            
            getGUIDTime = function () {
                return this.addZero(this.date.getHours()) + this.addZero(this.date.getMinutes()) + this.addZero(this.date.getSeconds()) + this.addZero(parseInt(this.date.getMilliseconds() / 10))
            }
            
            addZero = function (i) {
                return "NaN" != Number(i).toString() && i >= 0 && 10 > i ? "0" + Math.floor(i) : i.toString()
            }
            
            hexadecimal = function (i, e, t) {
                return void 0 != t ? parseInt(i.toString(), t).toString(e) : parseInt(i.toString()).toString(e)
            }
            
            formatGUID = function (i) {
                var e = i.slice(0, 8) + "-"
                    , t = i.slice(8, 12) + "-"
                    , a = i.slice(12, 16) + "-"
                    , o = i.slice(16, 20) + "-"
                    , n = i.slice(20);
                return e + t + a + o + n
            }
        
            
    return newGUID();
}
'''


def login(mobilePhone, pswd):
    guid = js2py.eval_js(js)
    cookies = dict()
    cookies['ud'] = guid()
    r = requests.post(login_url, cookies=cookies, headers=headers, data={
        'mobilePhone': mobilePhone,
        'pswd': pswd,
        'imageCode': ''
    })
    d = json.loads(r.text)
    c = d['result'].split('|')
    cookies['tok'] = c[0]
    cookies['u'] = c[1]
    cookies['m'] = c[2].replace("/", '%2F').replace("=", "%3D")
    # r2=requests.post(islogin_url,headers=headers,cookies=cookies)
    # print(r2.text)
    # ud tok u m
    return cookies

def get_auctionId(select_city,cookies):
    l=list()
    if(int(select_city)==1):
        cityValues='4,1760'
    else:
        cityValues=''
    for n in range(1,1000):
        print("获取id第%s页"%n)
        r = requests.post(cars_url, headers=headers,cookies=cookies,data={
            'status': 1,
            'brand':'',
            'cityValues':cityValues,
            'registerValues':'',
            'yearsValues':'',
            'clickCount': 0,
            'orderUp': 'asc',
            'orderBy':'',
            'currentPage': n,
        })
        s=BeautifulSoup(r.text,'lxml')
        cars=s.select(".pai-list .clearfix")
        if len(cars)==0:
            break
        for i in cars:
            spans=i.select("span")
            if(spans[-7].text in ['骨架：5星','骨架：4星','骨架：3星'] and spans[-2].text=='\n出价\n'):
                auctionId=i.select(".controls")[0]['data-id']
                l.append(auctionId)
    return l

def chujia(cookies,auctionId):
    r=requests.post(chujia_url,headers=headers,cookies=cookies,data={
        'price':100,
        'auctionId':auctionId
    })
    d=json.loads(r.text)
    return d

if __name__ =="__main__":
    mobilePhone = input("输入用户名：")
    pswd = input("输入密码：")
    select_city=input("选择（1.重庆、成都 2.全国）：")

    cookies=login(mobilePhone, pswd)
    print("登录成功！")
    auctionIds=get_auctionId(select_city,cookies)
    print("获取id成功！")
    chenggong=0
    chongfu=0
    shibai=0
    for i in auctionIds:
        try:
            a=chujia(cookies,i)
            if(a['code']==200):
                print("出价成功"+i)
                chenggong+=1
            elif(a['code']==500):
                print("重复出价"+i)
                chongfu+=1
            else:
                print("出价失败"+i)
                shibai+=1
        except:
            print("出价失败"+i)
            shibai+=1

    print("=============完成=============")
    print("成功%d个 重复%d个 失败%d个"%(chenggong,chongfu,shibai))
    print("          按回车退出")
    input()
