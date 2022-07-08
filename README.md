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

¡°mongodb+srv://<your user id>:<password>@cluster0.zu5gllz.mongodb.net/?retryWrites=true&w=majority¡±

Download mongodb and install it. Use mongoimport to import the dataset to your collection, the sample code should be  
mongoimport --uri "mongodb+srv://<username>:<userpassword>@cluster0.zu5gllz.mongodb.net/<databsename>?retryWrites=true&w=majority" --collection <collection¡· /drop /jsonArray /file:dataset/crime.json


