from flask import Flask

from datetime import datetime
import psycopg2
import urllib.parse as urlparse
import os
from flask.globals import request
from flask.templating import render_template

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )




app = Flask(__name__)

@app.route('/')
def homepage():
    

    return render_template('index.html')




@app.route('/set_magnetlink', methods = ['GET', 'POST'])
def setMagnet():
    cursordb = conn.cursor()
    if request.method == 'POST':
        url = request.form['url']
        cursordb.execute("""INSERT INTO descargas (magnetlink) VALUES ('""" + url +"""')""")
        cursordb.execute("""COMMIT""")
        return render_template('confirmation.html')
    return render_template('set_magnetlink.html')

@app.route('/get_magnetlink')
def getMagnet():
    cursordb = conn.cursor()
    cursordb.execute("""SELECT * FROM descargas""")
    result= cursordb.fetchall()
    return render_template('get_magnetlink.html', result = result)
            
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    
    
    
    

