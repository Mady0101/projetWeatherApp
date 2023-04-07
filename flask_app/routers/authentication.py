import json
import random
from flask import (Blueprint,request,session,flash,redirect,url_for,render_template)

from flask_app.models.user import User



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

        user = User(id=1, username='admin', password='admin',email='')
        
       
        if user:
            session['user'] = user.id
            return redirect(url_for('home_blueprint.home' , user= user))

        flash('Invalid username or password.')
        return redirect(url_for('.login'))

    return render_template('login.html')


@authentication_blueprint.route('/signup')
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not username or not password:
            flash('Please enter your username and password.')
            return redirect(".signup")

        # send signup to backend and check 
        # if any(user.username == username for user in users):
        #     flash('Username already exists.')
        #     return redirect(url_for('signup'))

        user = User(id=random.randint(2,100), username=username, password=password, email=email)
        
        # add to database
        # users.append(user)

        return redirect(url_for('profile'))
    return render_template('signup.html')

@authentication_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('.login'))

