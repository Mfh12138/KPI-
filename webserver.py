from flask import Flask, render_template, request, redirect
import db_operate
import json
import dingding

web_server = Flask('__name__', static_folder='', template_folder='templates')
# 进入登录界面
@web_server.route('/', methods=['GET'])
def index():
    return render_template('KPI.html')

# 进入主界面
@web_server.route('/main', methods=['GET'])
def show_main():
    return render_template('KPImain.html')

# 判断注册是否成功
@web_server.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if len(username) == 0 | len(password) == 0:
        # return render_template('KPI.html', message="用户名或者密码不能为空！")
        return redirect('/')
    res = db_operate.get_user(username, password)
    print(type(res), res)
    if res:
        print("登录成功！！")
        return redirect('/main')
    else:
        print("登录失败")
        return redirect('/')

@web_server.route('/register', methods=['POST'])
def register():
    # email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    if len(username) == 0 | len(password) == 0:
        print("用户名和密码为空！")
        return redirect('/')
    count = db_operate.getUserByName(username)
    if count <= 0:
        db_operate.insert_user(username, password)
        print("注册成功！！")
        return redirect('/')
    else:
        # 用户已经存在
        print("用户已存在，注册失败！！")
        return redirect('/')

@web_server.route('/yearAnay')
def yearAnay():
    result = db_operate.get_year()
    print(type(result), result)
    yearAnay = {}
    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    cnt4 = 0
    for year in result:
        if (year < '1990'):
            cnt1 += 1
        elif (year < '2000'):
            cnt2 += 1
        elif (year < '2010'):
            cnt3 += 1
        else:
            cnt4 += 1
    yearAnay.update({'90年代前': cnt1})
    yearAnay.update({'90年代': cnt2})
    yearAnay.update({'00年代': cnt3})
    yearAnay.update({'10年代': cnt4})
    print(type(yearAnay), yearAnay)
    # return json.dumps(yearAnay)
    result1 = db_operate.insert_year_count(yearAnay)
    print(type(result1), result1)

@web_server.route('/get_year_count')
def get_year_count():
    result = db_operate.get_year_count()
    print(type(result), result)
    return json.dumps(result)

@web_server.route('/get_heatMapData')
def getHeatMapData():
    rs = db_operate.getReliData()
    result = json.dumps(rs)
    return result

@web_server.route('/get_biankuang')
def getBianKuang():
    testdata = {
        "xiaoqu": "浙江警察学院",
        "city": "杭州"
    }
    result = json.dumps(testdata)
    print(type(result), result)
    return result

@web_server.route('/dingding', methods=['POST','GET'])
def dd():
    # message = request.form.get('msg')
    message1 = request.get_json("fugai")
    print(type(message1), message1)
    result = "大数据分析结果推送：\n\t\t弱覆盖率 = {}\n\t\t杭州小区价格={}元/平方米" \
             "\n\t\t杭州租房户数={}户".format(message1['fugai'], message1['hz_price'], message1['hushu'])
    message = "后台传送数据测试！"
    print(result)
    dingding.send_text_msg(result)
    return "success"

@web_server.route('/dingding_pic', methods=['POST','GET'])
def dd_pic():
    pic_name = request.args.get('myfile')  # 注意这里是args,获取url中的值
    print(pic_name)
    dingding.send_pic(pic_name)
    return "success"

if __name__ == '__main__':
    web_server.run(host='0.0.0.0', port=1238, debug=True)
