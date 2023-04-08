import json
import random
from flask import (Blueprint,request,session,flash,redirect,url_for,render_template)
from pymongo import MongoClient
from flask_app.models.user import User


client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["users"]


authentication_blueprint = Blueprint('authentication_blueprint', __name__)

@authentication_blueprint.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please enter your username and password.')
            return redirect(url_for('.login'))
        #get user from database or return null if not correct with status 200
        
        exist = collection.find_one({"username": username})
        if exist:
            if not exist.password == password:
                flash('username or password are wrong')
                return redirect(url_for('.login'))
        if not exist:
            flash('username or password are wrong')
            return redirect(url_for('.login'))
         

        user = User(exist.id, username=exist.username, password=exist.password,email=exist.email)
        session['user'] = user.id
        return redirect(url_for('home_blueprint.home' , user= user))

    return render_template('login.html')


@authentication_blueprint.route('/signup' , methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not username or not password:
            flash('Please enter your username and password.')
            return redirect(url_for('.signup'))

        exist = collection.find_one({"username": username})
        print("exist")
        print(exist)
        if exist:
            flash('username exist')
            return redirect(url_for('.signup'))
        
        collection.insert_one({"username": username, 'password': password, 'email': email})

        user = User(id=random.randint(2,100), username=username, password=password, email=email)
        
        # add to database
        # users.append(user)

        return redirect(url_for('home_blueprint.home'))
    return render_template('signup.html')

@authentication_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('.login'))

