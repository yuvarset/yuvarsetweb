# Back End Script deployed via Heroku
from flask import Flask, flash, redirect, render_template, request, url_for
#from flask_mysqldb import MySQL
import psycopg2
import datetime
import os
import smtplib
import imghdr
from email.message import EmailMessage

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# Database connection through Env Variables
mysql = psycopg2.connect(host=os.environ.get('MYSQL_HOST'),
                   user=os.environ.get('MYSQL_USER'),
                   password=os.environ.get('MYSQL_PASSWORD'),
                   database=os.environ.get('MYSQL_DB'))

# Html pages connection
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

        cur = mysql.cursor()
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
    cur = mysql.cursor()
    cur.execute(f"SELECT * from users WHERE username = '{login.username}'")
    rows = cur.fetchall()
    return render_template("user.html", rows=rows)

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/mailPass', methods=["POST"])
def mailPass():
    cur = mysql.cursor()
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
        msg.set_content(f"Hi {rows[0][2]} \n\nYour login details are as follows :\n     Username : {rows[0][0]} \n     Password : {rows[0][1]}\n\nPlease avoid repling to this email \nHave a great day \n\n\nKind Regards, \nTeam YUVA")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return  render_template("forgot.html",msg = 'Login details sent succesfully. Click to Login')
