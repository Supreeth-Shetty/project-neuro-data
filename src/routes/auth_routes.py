import MySQLdb
from flask import Blueprint, request, render_template, session, redirect, url_for
from app import mysql
import re

print("pankaj")
print(mysql)

auth_route = Blueprint('auth', __name__)

@auth_route.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tblUsers WHERE Email = % s AND Password = % s', (email, password,))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['UserId']
                session['username'] = account['Name']
                msg = 'Logged in successfully !'
                return render_template('index.html', msg=msg)
            else:
                msg = 'Incorrect username / password !'
        return render_template('login.html', msg=msg)


@auth_route.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tblUsers WHERE Email = % s', (email,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
            else:
                cursor.execute(f'INSERT INTO tblUsers(Name, Email, Password, AuthToken) VALUES ({username, email, password, "pankajtest"})')
                mysql.connection.commit()
                msg = 'You have successfully registered !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('register.html', msg=msg)


@auth_route.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

