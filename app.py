from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = os.urandom(21)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.route('/')
def index():
    if "logged_in" in session:
        if not session["logged_in"] is None:
            if session["logged_in"] == True:
                return render_template('index.html', username = session['username'])
    return render_template('index.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        if password == password2:
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO user_logins VALUES(%s,%s)''',(username, password,))
            mysql.connection.commit()
            cursor.close()
            return redirect("/")
        else:
            return redirect("/signup")



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT password FROM user_logins WHERE username=%s", (username,))
        right_password = cursor.fetchone()
        if right_password is not None:
            right_password = right_password[0]
            if password == right_password:
                session["logged_in"] = True
                session["username"] = username
                print("right Password")
            else:
                print("wrong Password!")
        else:
            print("wrong Username!")
        mysql.connection.commit()
        cursor.close()
        return redirect("/")
        
@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
