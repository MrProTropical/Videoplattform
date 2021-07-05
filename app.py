from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_mysqldb import MySQL
import os
import re
import logging

logging.basicConfig(filename='program.log', level=logging.DEBUG, format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
app.secret_key = os.urandom(21)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config["FILE_UPLOADS_PATH"] = '/static/uploads/'
app.config["ALLOWED_FILE_EXTENSIONS"] = [".JPEG", ".JPG", ".PNG", ".GIF"]

next_filename = 0

while os.path.isfile(app.config["FILE_UPLOADS_PATH"] + str(next_filename) + app.config["ALLOWED_FILE_EXTENSIONS"][0]) or os.path.isfile('uploads/' + str(next_filename) + app.config["ALLOWED_FILE_EXTENSIONS"][1]) or os.path.isfile('uploads/' + str(next_filename) + app.config["ALLOWED_FILE_EXTENSIONS"][2]) or os.path.isfile('uploads/' + str(next_filename) + app.config["ALLOWED_FILE_EXTENSIONS"][3]): #not very good code in this line
    next_filename += 1

mysql = MySQL(app)

def validateEmail(email):
    return re.match(r"[\w-]{1,20}@\w{2,20}\.\w{2,3}$", email)

@app.route('/')
def index():
    if "logged_in" in session:
        if not session["logged_in"] is None:
            if session["logged_in"] == True:
                return render_template('index.html', username = session['username'])
    return render_template('index.html', filename = app.config["FILE_UPLOADS_PATH"] + str(next_filename) + ".JPG") #not final code

@app.route('/upload', methods=['Get','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        global next_filename
        if request.files:
            uploadedfile = request.files["datei"]
            filename = uploadedfile.filename
            if filename == "":
                print("No filename!")
            else:
                if "." in filename:
                    extension = filename.rsplit(".", 1)[1]
                    extension = "." + extension.upper()
                    if extension in app.config["ALLOWED_FILE_EXTENSIONS"]:
                        while os.path.isfile(app.config["FILE_UPLOADS_PATH"] + str(next_filename) + app.config["ALLOWED_FILE_EXTENSIONS"][0]) or os.path.isfile('uploads/' + str(next_filename) + app.config["ALLOWED_FILE_EXTENSIONS"][1]) or os.path.isfile('uploads/' + str(next_filename) + app.config["ALLOWED_FILE_EXTENSIONS"][2]) or os.path.isfile('uploads/' + str(next_filename) + app.config["ALLOWED_FILE_EXTENSIONS"][3]): #not very good code in this line
                            next_filename += 1
                        filename = str(next_filename) + extension
                        uploadedfile.save(os.path.join(app.config["FILE_UPLOADS_PATH"], filename))
        return redirect("/")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        email = request.form["email"]
        password = request.form['password']
        password2 = request.form['password2']
        if password == password2 and validateEmail(email): # validateEmail(email) konnte nicht getestet werden, da in html bereits überprüft wird
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO user_logins VALUES(%s,%s,%s)''',(username, email, password,))
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
