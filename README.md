# web_app_python_flask  
web app develop with python and flask. Mongodb as the database, Chicago criminal record as the dataset. Pythonanywhere as the web server.  
You can go to the scuaaa.pythonanywhere.com/ad_search.html for the web sample.  
developed by buddi, i-chun, Wenjing

the website is like this.
![](pictures/web_page.png)  

# setup of the application  
1. build the database.  
Create a free account in [mongoDB atlas]( https://www.mongodb.com/cloud/atlas/register) for a free account. Then create a database based on a shared cluster. 
![](pictures/build_data_base.png)

Create the username and password of yourself. It will be used to connect to your database.  
![](pictures/user_password.png)  

Set the IP address 0.0.0.0/0, opening to any IP address.  
![](pictures/ip_set.png)

Go to database, and select Browse Collections. Then Add My Own Data. The database name and the collection name will be used to connected to your database.
![](pictures/create_collection.png)  

Now [import]( https://www.mongodb.com/docs/atlas/import/mongoimport/) the dataset chicago criminal data, First get the mongodb atlas connection uri. Click Databases in the top-left corner of Atlas. From the Database Deployments view, click Connect for the Atlas cluster into which you want to migrate data. Click Connect Your Application, and you can get uri like this.  

mongodb+srv://your user name:password@cluster0.zu5gllz.mongodb.net/?retryWrites=true&w=majority

![](pictures/uri.png)  


Download mongodb and install it. Use mongoimport to import the dataset to your collection, the sample code should be  
  
mongoimport --uri "mongodb+srv://username:userpassword@cluster0.zu5gllz.mongodb.net/<databsename>?retryWrites=true&w=majority" --collection your_collection /drop /jsonArray /file:dataset/crime.json  

If you download the mongodb compass, it will be much easier fir you to import the data.

2. setup the pythonanywhere web server.  
Create a account in the [pythonanywhere]( https://www.pythonanywhere.com/), your need a pay account to connect mongodb from the web server.But you can choose 5$/month.  
Using bash to get the repo first,  
git clone https://github.com/scuaaa/web_app_python_flask_mongodb  

create a virtual environment, we use python 3.9.  

mkdir virtual  

python3 -m venv virtual  

source virtual/bin/activate  

Then navigate to the repo, install the requirements by  

Pip install -r requirements.txt 

3. setup your env variables. First open the .env file in the repo, replacing the uri, database, collection to connect your mongodb database.

uri="mongodb+srv://user_name:password@atlascluster.4qnuciy.mongodb.net/?retryWrites=true&w=majority"  
database="test"  
collection="test"  

the code for python connect the mongdb atlas database are:  
  
uri2 = os.getenv('uri', "dev")  
database_name = os.getenv('database', "dev")  
collection_name = os.getenv('collection', "dev")  
client=MongoClient(uri2,connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)  
db=client[database_name]  
criminal = db[collection_name]  


4. Setup the web application. Selecting the web icon in the dashboard. Choose the Source code and the working directory to the repo directory. Also setup the Virtualenv to your virtual direction.   

![](pictures/web_setup.png)  

For the WSGI configuration file, open it and replace it as follow, or replace it with the content in wsgi_configure_file.py   

import sys  
path = '/home/scuaaa/web_app2/web_app_python_flask_mongodb'  # path to your repos  
if path not in sys.path:  
&ensp    sys.path.append(path)  
from wsgi import app as application  

5. set up the password. For the username and passwords, opening the file login_user2.py  
Changing the USERS as following.  
  
USERS = [{  
        "id": 1,  
        "name": 'tom',  
        "password": generate_password_hash('123')  
    }]  
