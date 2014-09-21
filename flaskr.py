# all the imports
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import os

# configuration
# developer has to create table first by using python shell
# >>from flaskr import init_db
# >> init_db() table is crated
DATABASE = '/Users/gongzhen/Virtualenvs/helloworld/flaskr/flaskr.db' #C:\Projects\flask\flaskr
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'gongzhen'
PASSWORD = 'gongzhen'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTING', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

# display the entries
# It bind with the root "/" 
# return dict
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/users')
def show_users():
    if not session.get('logged_in'):
        abort(401)

    cur = g.db.execute('select * from users order by id desc')
    users = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
    print users
    return render_template('show_users.html', users=users)

# add entries
# it only response POST request.
# the Form will display on show_entries.html
@app.route('/add', methods=['POST'])
def add_entry():                    
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


# login page
# if request method is POST and check username and password match with db.
# if not login, then redirect to show_entries page
# if login, then render page login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


# login page
# if request method is POST and check username and password match with db.
# if not login, then redirect to show_entries page
# if login, then render page login.html
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

# logout page
# session will remove logged_in key.
# we use pop method to delete key which from the dictonary 
# if logged_in key does not exist, then it will do nothing.
# flash logout information.

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug = DEBUG)