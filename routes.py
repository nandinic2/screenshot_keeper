from app import app
from flask import Flask, request, send_file, url_for, render_template, redirect, session, g
from flask_bootstrap import Bootstrap
from app.models import model
import pyautogui
import time

from flask_pymongo import PyMongo

app.config['SECRET_KEY'] = 'sanskriti2012'
app.config['MONGO_URI'] = 'mongodb+srv://admin:teesi5o1gOex2h5G@cluster0-n5tzk.mongodb.net/pictures?retryWrites=true&w=majority'
app.secret_key= 'b\x1f\x01\xc2\xa9\xd9\x02Cm\x85\x86'


mongo = PyMongo(app)
Bootstrap(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
#sign up
@app.route('/signup', methods=['POST', 'GET' ])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            users.insert({'name':request.form['username'], 'password': request.form['password']})
            session['username'] = request.form
            return redirect(url_for('index'))

        return 'That username already exists!'
    return render_template('signup.html')

#log in
@app.route('/login', methods=['POST'])
def login():
    #connects to users database
    users = mongo.db.users
    #queries through database to find saved user with the same username as inputted in the form.
    login_user = users.find_one({'name': request.form['username']})
    #if such username exists in the database
    if login_user:
        if request.form['password'] == login_user['password']:
            #start the user's session
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    #else
    return 'Invalid username/password combination'

#Log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/create',  methods = ['POST'])
def create():
    #retrieve screenshot posted from input template.
    screenshot = request.files['screenshot']
    #retrieves user’s username from the session.
    username = session.get('username')
    #prepares screenshot to be added to Mongo “pictures” database.
    mongo.save_file(screenshot.filename, screenshot)
    username = session.get('username')
    #retrieve name and category of screenshot posted from input template.
    category = request.form['category']
    #makes category input uppercase
    category = category.upper()
    file_name = request.form['file_name']
    #adds username, picture, category and file name to Mongo “pictures” database.
    mongo.db.pictures.insert({'username': username,'screenshot':screenshot.filename,'category': category,'file_name': file_name})
    return redirect(url_for('pictures'))

@app.route('/searched', methods = ['POST'])
def searched():
    search = request.form['search']
    #makes search input uppercase
    search = search.upper()
    #retrieves username from session
    username = session.get('username')
    #queries database to find all pictures under the entered category
    searched_terms = mongo.db.pictures.find({'username': username, 'category':search})
    return render_template('searched.html', searched_terms = searched_terms)


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/pictures')
def pictures():
    #check if session running
    if session.get('username', None) is not None:
        username = session.get('username')
        #query database using username
        pictures = list(mongo.db.pictures.find({'username':username}))
        #render pictures template and send all pictures found to template
        return render_template('pictures.html', pictures = pictures)
    else:
        return render_template('pictures.html')

@app.route('/input', methods=["GET"])
def input():
    return render_template('input.html')

#deleting
@app.route('/deleteAll', methods = ['Get','Post'])
def deleteAll():
    users = mongo.db.users
    #connects to the database
    collection = mongo.db.pictures
    userdata = dict(request.form)
    if userdata['name'] == '':
        #retrieve username from session
        username = session.get('username')
        password = userdata['password']
        #names password collected from form as password
        user = users.find_one({'name': username})
        passedword = user['password']
        if password == passedword:
            #deletes all entries in the database
            collection.delete_many({'username': username})
            #loads deleteAll.html
            return render_template('deleteAll.html')
    #if no password inputted
    elif userdata['password'] == '':
        #userdata only equal to name of file
        userdata = userdata['name']
        #delete specific file
        collection.delete_many({'file_name':userdata})
        return render_template('deleteAll.html')
    else:
        return 'Try again'
