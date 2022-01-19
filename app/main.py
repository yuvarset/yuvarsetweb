from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import datetime
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# Database connection
app.config["DEBUG"] = True
app.config["MYSQL_HOST"] = "sql6.freemysqlhosting.net"
app.config["MYSQL_USER"] = "sql6458625"
app.config["MYSQL_PASSWORD"] = "PpFuFC8nPT"
app.config["MYSQL_DB"] = "sql6458625"
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
