from flask import Flask, request, jsonify
from flask import render_template
from flask import redirect, render_template, session
from functools import wraps
import a
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)   #设置一个随机24位字符串为加密盐
app.config.update(TEMPLATE_AUTO_RELOAD=True)

# 装饰器装饰多个视图函数
def wrapper(func):
    @wraps(func)  # 保存原来函数的所有属性,包括文件名
    def inner(*args, **kwargs):
        # 校验session
        if session.get("cookies"):
            ret = func(*args, **kwargs)  # func = home
            return ret
        else:
            return redirect("/")
    return inner

@app.route('/',methods=['GET','POST'])
def index():
    return redirect("/login")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
    mobilePhone=request.form['phone']
    pswd=request.form['pwd']
    cookies=a.login(mobilePhone,pswd)

    if cookies == 'error':
        return 'error'

    session['cookies']=cookies
    session['mobilePhone']=mobilePhone
    session['pswd']=pswd
    # select_city=request.form['select_city']
    # worker(mobilePhone,pswd,select_city)

    return "success"

@app.route('/worker',methods=['GET','POST'])
@wrapper
def worker():
    if request.method=="GET":
        return render_template('worker.html')
    select_city=request.form['city']
    r=a.worker(session['cookies'],select_city)
    return r

@app.route('/worker1',methods=['POST'])
@wrapper
def worker1():
    d=dict()
    with open("a.txt","r+") as f:
        l=f.read().split('\n')
        for i in l:
            if(i==''):
                break
            s=i.split(' ')
            d[s[0]]=i
    
    select_city=request.form['city']
    time=request.form['time']
    flag=request.form['flag']

    d[session['mobilePhone']]="%s %s %s %s %s"%(session['mobilePhone'],session['pswd'],select_city,time,flag)
    
    with open("a.txt","w+") as f:
        for i in d:
            f.write(d[i]+'\n')

    return 'success'

@app.route('/get_status',methods=['POST'])
@wrapper
def get_status():
    d=dict()
    with open("a.txt","r+") as f:
        l=f.read().split('\n')
        for i in l:
            if(i==''):
                break
            s=i.split(' ')
            d[s[0]]=i
    if(session['mobilePhone'] in d):
        return jsonify(d[session['mobilePhone']].split(' '))
    else:
        return 'None'

if __name__ == '__main__':
    app.run(debug=True)