from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


main = Flask(__name__)


main.secret_key = 'abcdxyz'


main.config['MYSQL_HOST'] = 'localhost'
main.config['MYSQL_USER'] = 'root'
main.config['MYSQL_PASSWORD'] = '@Ag12112001@'
main.config['MYSQL_DB'] = 'flaskapp'


mysql = MySQL(main)


@main.route('/')
@main.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            msg='Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect email / password !'
    return render_template('login.html', msg = msg)


@main.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@main.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
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
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registration.html', msg = msg)


@main.route('/update', methods =['GET', 'POST'])
def update():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'username' in request.form:
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill all the fields !' 
        else:
            cursor.execute('UPDATE accounts SET username = % s, password = % s WHERE email = %s', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully update the values'
    elif request.method == 'POST':
        msg = 'Please fill all the fields !'        
    return  render_template('update.html', msg = msg)


if __name__=="__main__":
    main.run(debug=True)