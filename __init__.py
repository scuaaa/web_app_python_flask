import os
from flask import Flask
from flask import escape, url_for, render_template, request, redirect, flash
from flask_login import login_user
from flask import send_file, make_response, send_from_directory
from flask_login import current_user, login_required
from flask_login import logout_user
from .login_user2 import *


app = Flask(__name__)
app.secret_key = 'abc'
login_manager = LoginManager() 
login_manager.init_app(app)
login_manager.login_view = 'login'

from pymongo import MongoClient


uri2 = "mongodb+srv://Wenjing:t13550230197@project.oviin7k.mongodb.net/?retryWrites=true&w=majority"

client=MongoClient(uri2)
db=client["test-DB"]
criminal = db["crime"]

@app.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



insert_result=[]
atrribute = ["Case Number","Date","Block","Primary Type","Description","Location Description",
            "Arrest","District","Ward","Community Area","X Coordinate","Y Coordinate","Year","Latitude","Longitude",
            "Location"]
@app.route('/insert.html', methods=["GET",'POST'])
@login_required
def insert():
    if request.method == 'POST': 
        case = {}
        for atr in atrribute:
            value = request.form.get(atr)
            case[atr] = value
        criminal.insert_one(case)

        global insert_result
        insert_result=[]

        insert_result.append(case)
        return redirect(url_for('insert'))  # 重定向回主页

    return render_template('insert.html', username=current_user.username,results=insert_result,atrrbute=atrribute)



@app.route('/update.html', methods=["GET",'POST'])
@login_required
def update():
    if request.method == 'POST':  # 判断是否是 POST 请求
        case = {}
        for atr in atrribute:
            value = request.form.get(atr)
            case[atr] = value
        result = search_results[0]
        update_case = {"$set":case}
        criminal.update_one(result,update_case)
        search_results[0] = case


        return redirect(url_for('update'))  # 重定向回主页

    return render_template('update.html', username=current_user.username, results=search_results , atrrbute=atrribute)


esm2 = "noting to do"

@app.route('/deleteupdate.html', methods=["GET",'POST'])
@login_required
def admin():
    
    if request.method == 'POST':  # 判断是否是 POST 请求
        global esm2
        esm2 = "noting to do"
        action = request.form.get('id_name')   # 传入表单对应输入字段的 name 值
        # 验证数据

        # 保存表单数据到数据库
        if action == "search":
            global search_results
            search_results = []
            case = request.form.get('caseid')
            search = criminal.find({"Case Number": case})
            for result in search:
                search_results.append(result)

            return redirect(url_for('admin'))  # 重定向回主页
        
        if action == "delete":
            for result in search_results:
                criminal.delete_one(result)
            
            esm2 = "successful delete"
            return redirect(url_for('admin'))
            

    return render_template('deleteupdate.html', username=current_user.username,results=search_results , atrrbute=atrribute,esmg =esm2)


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)


@app.route('/admin.html', methods=["GET",'POST'])
def login():
    form = LoginForm()
    emsg = None
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_info = get_user(user_name)  # 从用户数据中查找用户记录
        if user_info is None:
            emsg = "username or password error"
        else:
            user = User(user_info)  # 创建用户实体
            if user.verify_password(password):  # 校验密码
                login_user(user)  # 创建用户 Session
                return redirect(request.args.get('next') or url_for('admin'))
            else:
                emsg = "username or password error"
    return render_template('admin.html', form=form, emsg=emsg)


t_results =[]
@app.route('/criminaltime.html', methods=["GET",'POST'])
def t_search():
    if request.method == 'POST':  # 判断是否是 POST 请求
        global t_results
        t_results = []

        search_word = request.form.get("criminaltime")

        # 验证数据
        search = criminal.find({"Date": search_word})
        for result in search:
            t_results.append(result)
        return redirect(url_for('t_search'))  # 重定向回主页

    return render_template('criminaltime.html', results=t_results)




ct_results =[]
ct_dict = {"Primary Type":"criminal type","Description":"Description"}

@app.route('/criminaltype.html', methods=["GET",'POST'])
def ct_search():
    if request.method == 'POST':  # 判断是否是 POST 请求
        global ct_results
        ct_results = []

        id_n = request.form.get('id_name')
        case = ct_dict[id_n]
        search_word = request.form.get(case)

        # 验证数据
        search = criminal.find({id_n: search_word})
        for result in search:
            ct_results.append(result)
        return redirect(url_for('ct_search'))  # 重定向回主页

    return render_template('criminaltype.html', results=ct_results)


ld_results=[]
ld_dict = {"District":"district","Block":"block","Ward":"ward","Community Area":"Community Area"}


@app.route('/location.html', methods=["GET",'POST'])
def ld_search():
    if request.method == 'POST':  # 判断是否是 POST 请求
        id_n = request.form.get('id_name')
        case = ld_dict[id_n]
        search_word = request.form.get(case)
        print(search_word)
        global ld_results
        ld_results = []
        # 验证数据
        search = criminal.find({id_n: search_word})
        for result in search:
            ld_results.append(result)
        return redirect(url_for('ld_search'))  # 重定向回主页

    return render_template('location.html', results=ld_results)




id_results=[]

@app.route('/caseid.html', methods=["GET",'POST'])
def id_search():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        global id_results
        id_results = []
        case = request.form.get('caseid')  # 传入表单对应输入字段的 name 值
        # 验证数据
        if not case:  # 显示错误提示
            return redirect(url_for('hello'))  # 重定向回主页
        # 保存表单数据到数据库
        search = criminal.find({"Case Number": case})
        for result in search:
            id_results.append(result)

        return redirect(url_for('id_search'))  # 重定向回主页

    return render_template('caseid.html', results=id_results)


search_results=[]

@app.route('/search', methods=["GET",'POST'])
def search():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        global search_results
        search_results = []
        case = request.form.get('case_number')  # 传入表单对应输入字段的 name 值
        # 验证数据
        if not case:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('hello'))  # 重定向回主页
        # 保存表单数据到数据库
        search = criminal.find({"Case Number": case})
        for result in search:
            search_results.append(result)

        return redirect(url_for('search'))  # 重定向回主页

    return render_template('search.html', results=search_results)


ad_search_results=[]

@app.route('/ad_search.html', methods=["GET",'POST'])
def ad_search():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        global ad_search_results
        ad_search_results = []

        criminal_type = request.form.get('criminal type')
        criminal_time = request.form.get('criminaltime')
        district = request.form.get('district')  # 传入表单对应输入字段的 name 值
        # 验证数据
        type(criminal_type)

        if not criminal_type:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('hello'))  # 重定向回主页
        

        if criminal_type and criminal_time and district:
            search = criminal.find({'Primary Type': criminal_type, "District": district ,"Date":criminal_time})
            for result in search:
                ad_search_results.append(result)

        elif criminal_type and criminal_time:
            search = criminal.find({'Primary Type': criminal_type,"Date":criminal_time})
            for result in search:
                ad_search_results.append(result)

        elif criminal_type and district:
            search = criminal.find({'Primary Type': criminal_type,"District":district})
            for result in search:
                ad_search_results.append(result)


        elif criminal_type:
            search = criminal.find({'Primary Type': criminal_type})
            for result in search:
                ad_search_results.append(result)

        return redirect(url_for('ad_search'))  # 重定向回主页

    return render_template('ad_search.html', results=ad_search_results)

@app.route('/<report_id>', methods=['GET'])
def post(report_id):
    headers = ("Content-Disposition", f"inline;filename={report_id}")#文件预览
    as_attachment = False
    # headers = (f"Content-Disposition", f"attachement;filename={report_id}.pdf")#文件下载
    # as_attachment = True
    file_path ='static/{}'.format(str(report_id))
    response = make_response(send_file(path_or_file =file_path, as_attachment=as_attachment))
    response.headers[headers[0]] = headers[1]
    return response




@app.route('/', methods=["GET",'POST'])
def hello():
    return render_template('index_5.html')



@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = "scu_aaa"
    return render_template('404.html', user=user), 404  # 返回模板和状态码





