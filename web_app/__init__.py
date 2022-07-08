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


uri2 = os.getenv('uri', "dev")
database_name = os.getenv('database', "dev")
collection_name = os.getenv('collection', "dev")

client=MongoClient(uri2,connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db=client["test-DB"]
criminal = db["crime"]

@app.route('/logout') 
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
        return redirect(url_for('insert'))  

    return render_template('insert.html', username=current_user.username,results=insert_result,atrrbute=atrribute)



@app.route('/update.html', methods=["GET",'POST'])
@login_required
def update():
    if request.method == 'POST':  
        case = {}
        for atr in atrribute:
            value = request.form.get(atr)
            case[atr] = value
        result = search_results[0]
        update_case = {"$set":case}
        criminal.update_one(result,update_case)
        search_results[0] = case


        return redirect(url_for('update'))  

    return render_template('update.html', username=current_user.username, results=search_results , atrrbute=atrribute)


esm2 = "noting to do"

@app.route('/deleteupdate.html', methods=["GET",'POST'])
@login_required
def admin():

    if request.method == 'POST':  
        global esm2
        esm2 = "noting to do"
        action = request.form.get('id_name')   
        global search_results



        if action == "search":
            search_results = []
            case = request.form.get('caseid')
            search = criminal.find({"Case Number": case})
            for result in search:
                search_results.append(result)

            return redirect(url_for('admin'))  

        if action == "delete":
            for result in search_results:
                criminal.delete_one(result)
            search_results = []
            esm2 = "successful delete"
            return redirect(url_for('admin'))


    return render_template('deleteupdate.html', username=current_user.username,results=search_results , atrrbute=atrribute,esmg =esm2)


@login_manager.user_loader  
def load_user(user_id):
    return User.get(user_id)


@app.route('/admin.html', methods=["GET",'POST'])
def login():
    form = LoginForm()
    emsg = None
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_info = get_user(user_name)  
        if user_info is None:
            emsg = "username or password error"
        else:
            user = User(user_info)  
            if user.verify_password(password):  
                login_user(user)  
                return redirect(request.args.get('next') or url_for('admin'))
            else:
                emsg = "username or password error"
    return render_template('admin.html', form=form, emsg=emsg)


t_results =[]
@app.route('/criminaltime.html', methods=["GET",'POST'])
def t_search():
    if request.method == 'POST':  
        global t_results
        t_results = []

        search_word = request.form.get("criminaltime")

        
        search = criminal.find({"Date": search_word})
        for result in search:
            t_results.append(result)
        return redirect(url_for('t_search'))  

    return render_template('criminaltime.html', results=t_results)




ct_results =[]
ct_dict = {"Primary Type":"criminal type","Description":"Description"}

@app.route('/criminaltype.html', methods=["GET",'POST'])
def ct_search():
    if request.method == 'POST':  
        global ct_results
        ct_results = []

        id_n = request.form.get('id_name')
        case = ct_dict[id_n]
        search_word = request.form.get(case)


        search = criminal.find({id_n: search_word})
        for result in search:
            ct_results.append(result)
        return redirect(url_for('ct_search')) 

    return render_template('criminaltype.html', results=ct_results)


ld_results=[]
ld_dict = {"District":"district","Block":"block","Ward":"ward","Community Area":"Community Area"}


@app.route('/location.html', methods=["GET",'POST'])
def ld_search():
    if request.method == 'POST':  
        id_n = request.form.get('id_name')
        case = ld_dict[id_n]
        search_word = request.form.get(case)
        print(search_word)
        global ld_results
        ld_results = []

        search = criminal.find({id_n: search_word})
        for result in search:
            ld_results.append(result)
        return redirect(url_for('ld_search')) 

    return render_template('location.html', results=ld_results)




id_results=[]

@app.route('/caseid.html', methods=["GET",'POST'])
def id_search():
    if request.method == 'POST':  

        global id_results
        id_results = []
        case = request.form.get('caseid')  

        if not case:  
            return redirect(url_for('hello'))  

        search = criminal.find({"Case Number": case})
        for result in search:
            id_results.append(result)

        return redirect(url_for('id_search'))  

    return render_template('caseid.html', results=id_results)


search_results=[]

@app.route('/search', methods=["GET",'POST'])
def search():
    if request.method == 'POST':  

        global search_results
        search_results = []
        case = request.form.get('case_number')  

        if not case:
            flash('Invalid input.')  
            return redirect(url_for('hello'))  

        search = criminal.find({"Case Number": case})
        for result in search:
            search_results.append(result)

        return redirect(url_for('search')) 

    return render_template('search.html', results=search_results)


ad_search_results=[]

@app.route('/ad_search.html', methods=["GET",'POST'])
def ad_search():
    if request.method == 'POST':  

        global ad_search_results
        ad_search_results = []

        criminal_type = request.form.get('criminal type')
        criminal_time = request.form.get('criminaltime')
        district = request.form.get('district')  

        type(criminal_type)

        if not criminal_type:
            flash('Invalid input.')  
            return redirect(url_for('hello'))  


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

        return redirect(url_for('ad_search'))  

    return render_template('ad_search.html', results=ad_search_results)

@app.route('/<report_id>', methods=['GET'])
def post(report_id):
    headers = ("Content-Disposition", f"inline;filename={report_id}")
    as_attachment = False
    file_path ='static/{}'.format(str(report_id))
    response = make_response(send_file(path_or_file =file_path, as_attachment=as_attachment))
    response.headers[headers[0]] = headers[1]
    return response




@app.route('/', methods=["GET",'POST'])
def hello():
    return render_template('index_5.html')



@app.errorhandler(404)  
def page_not_found(e):  
    user = "scu_aaa"
    return render_template('404.html', user=user), 404  


