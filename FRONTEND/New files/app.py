from flask import Flask, render_template, request
from flask_mysqldb import MySQL
#from werkzeug.wrappers import request
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)

app.config['MYSQL_HOST']  = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Newconnect'  # db name

mysql = MySQL(app)
'''
@app.route('/')
def tryrdd():
    return "dfdf"
'''


@app.route('/dfd')
def tryrdfd():
    nums = 1
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Register WHERE num= % s', (nums, ))
    account = cursor.fetchone()
    print(account['email'])
    return "1"
if __name__=="__main__":
    app.run(debug=True)

