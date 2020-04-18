import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import js2py
import time
import sys


def Beijing_time():
    r = requests.get('https://www.baidu.com')
    t = time.strptime(r.headers['date'], '%a, %d %b %Y %H:%M:%S GMT')
    return time.mktime(t)+28800

# if(Beijing_time()>1587044401.6949608+86400):
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
# mobilePhone: 13677615580
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

isbid_url = "https://pai.ttpai.cn/bid/isbids"
# GET

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

    if d['code'] != 200:
        return 'error'

    c = d['result'].split('|')
    cookies['tok'] = c[0]
    cookies['u'] = c[1]
    cookies['m'] = c[2].replace("/", '%2F').replace("=", "%3D")
    # r2=requests.post(islogin_url,headers=headers,cookies=cookies)
    # print(r2.text)
    # ud tok u m
    return cookies


def get_isbids(cookies, auctionIds):
    r = requests.get(isbid_url, headers=headers, cookies=cookies,
                     params={'auctionIds': auctionIds})
    d = json.loads(r.text)
    l = list()
    if d['result'] == None:
        return []
    for i in d['result']:
        l.append(str(i['auctionId']))
    return l


brands = ['奥迪' ,'阿尔法罗密欧', '阿斯顿・马丁',
'标致' ,'本田' ,'宝马' ,'北京', '奔驰' ,'布加迪', '别克' ,'宾利' ,'保时捷' ,'比亚迪', '奔腾' ,'宝骏', '巴博斯' ,'北汽威旺' ,'北汽制造' ,'北汽绅宝', '北汽幻速' ,'北汽新能源' ,'宝沃',
'长安' ,'长城', '长安商用' , '长安轻型车' ,
'大众' ,'东风' ,'道奇' ,'东南' ,'东风风神' ,'东风风行', 'DS', '东风风度', '东风风光',
'丰田', '福特', '菲亚特', '法拉利', '福田',
'广汽传祺', 'GMC' ,'观致',
'悍马', '海马' ,'华泰' ,'红旗', '黄海', '海格' ,'哈弗' ,'汉腾汽车',
'吉利汽车' ,'捷豹' ,'Jeep', '金杯' ,'江淮' ,'江铃' ,'金龙' ,'金旅' ,'捷途' ,'几何汽车',
'克莱斯勒' ,'凯迪拉克' ,'科尼赛克', '凯翼' ,
'雷诺', '兰博基尼' ,'路虎' ,'林肯', '雷克萨斯' ,'铃木' ,'劳斯莱斯', '猎豹汽车', '力帆汽车' ,'陆风', '莲花汽车',  '理念' ,'领克',
'MG' ,'迈巴赫' ,'MINI' ,'玛莎拉蒂' ,'马自达',
'纳智捷',
'欧宝' ,'讴歌', '欧朗', '欧联' ,'欧拉', '欧尚汽车',
'奇瑞', '起亚', '启辰',
'荣威' ,'日产',
'smart' , '斯巴鲁', '斯柯达','三菱', '双龙' ,'上汽大通' ,'思铭' ,'斯威汽车',
'特斯拉',
'沃尔沃', '五菱汽车' ,'五十铃' ,'WEY', '蔚来',
'现代' ,'雪佛兰' ,'雪铁龙' ,'西雅特' ,'小鹏汽车' ,'鑫源' ,'星途' ,'新宝骏',
'英菲尼迪' ,'野马汽车' ,'依维柯' ,'驭胜',
'中华' ,'众泰'
]


def get_auctionId(select_city, cookies):
    l = list()
    if(int(select_city) == 1):
        cityValues = '4,1760'
    else:
        cityValues = ''
    for n in range(1, 50):
        print("获取id第%s页" % n)
        r = requests.post(cars_url, headers=headers, cookies=cookies, data={
            'status': 1,
            'brand': '',
            'cityValues': cityValues,
            'registerValues': '',
            'yearsValues': '',
            'clickCount': 0,
            'orderUp': 'asc',
            'orderBy': '',
            'currentPage': n
        })
        s = BeautifulSoup(r.text, 'lxml')
        cars = s.select(".pai-list .clearfix")
        if len(cars) == 0:
            break
        gujia_more3 = list()
        temp_l = list()
        for i in cars:
            spans = i.select("span")
            brand= spans[0].text.split(' ')[0]
            year=spans[1].select('strong')[0].text.strip().split('年')[0]

            if(spans[-7].text in ['骨架：5星', '骨架：4星', '骨架：3星'] and (brand in brands)):
                try:
                    if( (brand in ['大众','马自达','日产','奥迪','本田','宝马','奔驰','丰田'] and int(year) >=2008) or (brand in ['长安商用','长安轻型车','五菱汽车','金杯','吉利汽车','奇瑞','海马','力帆汽车','中华','众泰','长安'] and int(year) >=2013) or int(year)>=2010):
                        auctionId = i.select(".controls")[0]['data-id']
                        marketId = i.select(".controls")[0]['data-marketid']
                        gujia_more3.append((auctionId, marketId))
                        temp_l.append(auctionId)
                        print(brand,year)
                except:
                    continue

        auctionIds = ''
        for i in gujia_more3:
            auctionIds += i[1]+"_"+i[0]+','
        bids = get_isbids(cookies, auctionIds)
        l += list(set(temp_l)-set(bids))
    return list(set(l))


def chujia(cookies, auctionId):
    r = requests.post(chujia_url, headers=headers, cookies=cookies, data={
        'price': 100,
        'auctionId': auctionId
    })
    d = json.loads(r.text)
    return d


def worker(cookies, select_city):
    chenggong = 0
    chongfu = 0
    shibai = 0
    auctionIds1 = get_auctionId(select_city, cookies)
    auctionIds2 = get_auctionId(select_city, cookies)
    auctionIds=list(set(auctionIds1+auctionIds2))
    print("获取id成功！")
    for i in auctionIds:
        try:
            a = chujia(cookies, i)
            if(a['code'] == 200):
                print(a['message']+i)
                chenggong += 1
            else:
                print(a['message']+i)
                shibai += 1
        except:
            print("出价失败"+i)
            shibai += 1
    print("=============完成=============")
    print("成功%d个 失败%d个" % (chenggong, shibai))
    return "成功%d个 失败%d个" % (chenggong, shibai)


def worker_time(mobilePhone, pswd, select_city):
    cookies = login(mobilePhone, pswd)
    print("登录成功！")
    worker(cookies, select_city)


if __name__ == "__main__":
    # mobilePhone = input("输入用户名：")
    # pswd = input("输入密码：")
    # select_city=input("选择（1.重庆、成都 2.全国）：")

    # cookies=login(mobilePhone, pswd)
    # print("登录成功！")
    # worker(cookies,select_city)
    # print("          按回车退出")
    # input()

    d = dict()
    while(1):
        with open("a.txt", "r+") as f:
            l = f.read().split('\n')
            for i in l:
                if(i == ''):
                    break
                s = i.split(' ')
                d[s[0]] = i

        now_time = time.strftime("%H:%M", time.localtime())
        print("正在运行…… %s" % now_time)
        time.sleep(10)
        for i in d:
            s = d[i].split(' ')
            if(s[4] == '1' and s[3] == now_time):
                worker_time(s[0], s[1], s[2])
