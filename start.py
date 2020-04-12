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

if __name__ == '__main__':
    app.run(debug=True)