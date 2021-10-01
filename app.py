import cassandra
from flask import Flask, redirect, url_for, render_template, request, session
import re
from src.utils.mysql_helper import MySqlHelper
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import time
import pandas as pd
from src.utils.cassandra_helper import CassandraHelper

"""
Sql Connection
"""
mysql = MySqlHelper('38.17.53.115', '17652', 'admin', 'AsiK9wJ4', 'auto_neuron')
cassandra=CassandraHelper()

template_dir = 'src/templates'
static_dir = 'src/static'

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

"""
Project Configs
"""

app.secret_key = 'DB128%^#*(%$ZXC345'
app.config["UPLOAD_FOLDER"] = "src/store"
app.config["MAX_CONTENT_PATH"] = "209715200"


"""
    [summary]: Route for dashboard
    Returns:
        [type]: [Redirect to login or dashboard]
"""
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if 'loggedin' in session:
            return render_template('index.html')
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)

"""
[summary]:Route for create new project

    Returns:
        [type]: [description]
"""
@app.route('/project', methods=['GET', 'POST'])
def project():
    try: 
        if 'loggedin' in session:
            if request.method == "GET":
                return render_template('new_project.html')
            else:
                name = request.form['name']
                description = request.form['description']
                f = request.files['file']

                ALLOWED_EXTENSIONS = ['csv', 'tsv', 'json', 'xml']
                msg = ''
                if not name.strip():
                    msg = 'Please enter project name'
                elif not description.strip():
                    msg = 'Please enter project description'
                elif f.filename.strip() == '':
                    msg = 'Please select a file to upload'
                elif f.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
                    msg = 'This file format is not allowed, please select mentioned one'

                if msg:
                    return render_template('new_project.html', msg=msg)

                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                timestamp =round(time.time() * 1000)
                table_name = f"{name}_{timestamp}"
                file = f"src/store/{filename}"

                if filename.endswith('csv'):
                   status= cassandra.push_csv_to_database(file,table_name)
                   print(cassandra.retrive_dataset(table_name))

                if status==1:
                       userId = session.get('id')
                       status = 1
                       query=f"""INSERT INTO tblProjects (UserId, Name, Description, Status, 
                       Cassandra_Table_Name) VALUES
                       ("{userId}", "{name}", "{description}", "{status}", "{table_name}")"""
                       
                       rowcount = mysql.insert_record(query)
                       
                       if rowcount > 0:
                           return redirect(url_for('index'))
                       else:
                           msg="Error while creating new Project"

                return render_template('new_project.html',msg=msg)
        else:
            return redirect(url_for('login'))
    
    except Exception as e:
        print(e)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            account = mysql.fetch_one(f'SELECT * FROM tblUsers WHERE Email = "{email}" AND Password = "{password}"')
            if account:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                return redirect('/')
            else:
                msg = 'Incorrect username / password !'
        return render_template('login.html', msg=msg)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        msg = ''

        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm-password']
            email = request.form['email']
            account = mysql.fetch_one(f'SELECT * FROM tblUsers WHERE Email = "{email}"')
            if account:
                msg = 'EmailId already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
            elif confirm_password != password:
                msg = 'Password and Confirm password are not same!'
            else:
                rowcount = mysql.insert_record(f'INSERT INTO tblUsers (Name, Email, Password, AuthToken) VALUES ("{username}", "{email}", "{password}", "pankajtest")')
                if rowcount > 0:
                    return redirect(url_for('login'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('signup.html', msg=msg)


@app.route('/deletePage/<id>', methods=['GET'])
def renderDeleteProject(id):
    return render_template('deleteProject.html', data={"id": id})


@app.route('/deleteProject/<id>', methods=['GET'])
def deleteProject(id):
    print(id)
    if id:
        mysql.delete_record(f'DELETE FROM tblProjects WHERE Id={id}')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/stream')
def stream():
   return render_template('stream.html')



if __name__=='__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
