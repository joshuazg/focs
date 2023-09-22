from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
import boto3

customhost = "focsdb.cpkr5ofaey5p.us-east-1.rds.amazonaws.com"
customuser = "admin"
custompass = "admin123"
customdb = "focsDB"
custombucket = "semfocs-bucket"
customregion = "us-east-1"


app = Flask(__name__, static_folder='assets')

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('courses.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare_products():
    if request.method == 'POST' or request.method == 'GET':
        program_level = request.form.get('program_level') or request.args.get('program_level')

        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM Programme WHERE lvl_name = ?', (program_level,))
        prog = cursor.fetchall()
        cursor.close()

        return render_template('compare.html', program=prog)

    return render_template('compare.html', products=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

