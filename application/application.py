import flask
import os
from flask_mysqldb import MySQL
 
application = flask.Flask(__name__)
# engine = sqlalchemy.create_engine("mysql+pymysql://yentim0519:helloyen@database-1.crc98fdcbodi.us-east-2.rds.amazonaws.com/innodb")
# db = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(bind=engine))  # 這行出問題
# Config MySQL
application.config['MYSQL_HOST'] = 'database-1.crc98fdcbodi.us-east-2.rds.amazonaws.com'
application.config['MYSQL_USER'] = 'yentim0519'
application.config['MYSQL_PASSWORD'] = 'helloyen'
application.config['MYSQL_DB'] = 'innodb'
application.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(application)


@application.route('/')
def index():
    return flask.render_template('index.html')
    
@application.route('/result', methods=["POST"])
def result():
    brand_name = flask.request.form['brand_name']
    # top_notes = flask.request.form['top_notes']
    # middle_notes = flask.request.form['middle_notes']
    # base_notes = flask.request.form['base_notes']

    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM perfume_data WHERE product_brand LIKE '%{brand_name}%' or top_notes LIKE '%{brand_name}%' or middle_notes LIKE '%{brand_name}%' or base_notes LIKE '%{brand_name}%' '''.format(brand_name = brand_name))
    # 一定要用.format
    brand_datas = cur.fetchall()
    return flask.render_template('page1.html', brand_datas = brand_datas)

@application.route('/result1', methods=["POST"])
def result1():
    top_notes = flask.request.form['top_notes']
    middle_notes = flask.request.form['middle_notes']
    base_notes = flask.request.form['base_notes']

    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM perfume_data WHERE top_notes LIKE '%{top_notes}%' and middle_notes LIKE '%{middle_notes}%' and base_notes LIKE '%{base_notes}%' '''.format(top_notes = top_notes, middle_notes = middle_notes, base_notes = base_notes))
    brand_datas = cur.fetchall()
    return flask.render_template('page2.html', brand_datas = brand_datas)



if __name__ == '__main__':
    application.run(host='0.0.0.0')
