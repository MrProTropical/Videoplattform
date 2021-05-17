from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(21)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config["FILE_UPLOADS_PATH"] = 'uploads'
app.config["ALLOWED_FILE_EXTENSIONS"] = ["TXT", "JPEG", "JPG", "PNG", "GIF"]

mysql = MySQL(app)

def allowed_files(filename):

    if not "." in filename:
        return False

    extension = filename.rsplit(".", 1)[1]

    if extension.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/')
def index():
    if "logged_in" in session:
        if not session["logged_in"] is None:
            if session["logged_in"] == True:
                return render_template('index.html', username = session['username'])
    return render_template('index.html')

@app.route('/upload', methods=['Get','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        if request.files:
            uploadedfile = request.files["datei"]
            if uploadedfile.filename == "":
                print("No filename")
            else:
                if allowed_files(uploadedfile.filename):
                    filename = secure_filename(uploadedfile.filename)
                    if filename:
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
        if password == password2:
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO user_logins VALUES(%s,%s)''',(username, password,))
            mysql.connection.commit()
            cursor.close()
            return redirect("/")
        else:
            return redirect("/signup")
            
def validateEmail(email):
    return re.match(r"[\w-]{1,20}@\w{2,20}\.\w{2,3}$", email)
email = "hanswurst@gmail.com"
valid = validateEmail(email)
if valid:
    print(email, "is correct")
else:
    print("invalid email format:", email)


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
