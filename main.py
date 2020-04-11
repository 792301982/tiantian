from flask import Flask, request, jsonify
from flask import render_template
from flask import redirect, render_template, session
from a import *

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def a():
    if request.method=="GET":
        return render_template('a.html')
    mobilePhone=request.form['phone']
    pswd=request.form['pwd']

    cookies=login(mobilePhone, pswd)
    auctionIds=get_auctionId()
    for i in auctionIds:
        try:
            a=chujia(cookies,i)
            if(a['code']==200):
                print("出价成功"+i)
            elif(a['code']==500):
                print("重复出价"+i)
            else:
                print("出价失败"+i)
        except:
            print("出价失败"+i)
    print("=============完成=============")
    return "完成"

if __name__ == '__main__':
    app.run(debug=True)