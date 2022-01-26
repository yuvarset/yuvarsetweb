from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import datetime
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# Database connection through Heroku
app.config["DEBUG"] = True
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# html pages connection
@app.route('/', methods=['GET', 'POST'])
def index():
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    return render_template('index.html', currentYear=year)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':

        cur = mysql.connection.cursor()
        login.username = request.form['username']
        statement = f"SELECT username from users WHERE username='{login.username}' AND Password = '{request.form['password']}';"
        cur.execute(statement)
        if not cur.fetchone():
            error = 'Invalid username or password. Please try again!'

        else:
            flash('You were successfully logged in')
            return redirect(url_for('user'))

    return render_template('login.html', error=error)


@app.route('/user')
def user():
    con = mysql.connection
    cur = con.cursor()
    cur.execute(f"SELECT * from users WHERE username = '{login.username}'")
    rows = cur.fetchall()
    return render_template("user.html", rows=rows)

# Forgot Credentials Functionality
@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/mailPass', methods=["POST"])
def mailPass():
    con = mysql.connection
    cur = con.cursor()
    cur.execute(f"SELECT * from users WHERE email = '{request.form['email']}'")
    rows = list(cur.fetchall())
    if len(rows) == 0:
        return render_template("forgot.html", msg='Email not registered, Click to go back')
    else:
        EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
        EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

        msg = EmailMessage()
        msg['Subject'] = '[YUVA SUPPORT] Login Details for YMMS'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = request.form['email']
        msg.set_content(f"Hi {rows[0]['name']} \n\nYour login details are as follows :\n     Username : {rows[0]['username']} \n     Password : {rows[0]['password']}\n\nPlease avoid repling to this email \nHave a great day \n\n\nKind Regards, \nTeam YUVA")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return  render_template("forgot.html",msg = 'Login details sent succesfully. Click to Login')