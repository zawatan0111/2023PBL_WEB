from flask import Flask, render_template, request

#flaskオブジェクトの作成
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html',  title="ポイントカード照会ページ",  message="ポイントカード番号を入力")

@app.route('/', methods=['POST'])
def form():
	field = request.form['field']
	return render_template('index.html', title="%s さんのポイントカード照会ページ" % field,  message="保有ポイント : ")


@app.route('/form_1', methods=['GET'])
def form_1():
    return render_template('form_1.html')

@app.route('/form_1', methods=['POST'])
def form_1_P():
    content = request.form['content']
    return render_template('form_1_request.html', form_1_content="%s" % content)

@app.route('/price')
def price():
    return render_template('price.html')


#pythonで実行されたときに処理をする
if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost') 

#DB
import MySQLdb

#def connect():      
con = MySQLdb.connect(
	host = "localhost",
	user = "root",
	passwd = "20030111",
	db = "super_point"
)
#	return con

#con = connect()

cur = con.cursor()

cur.execute("""
			CREATE TABLE super_point.user(
            id MEDIUMINT NOT NULL AUTO_INCREMENT,
            user_name VARCHAR(30),
            password VARCHAR(30),
            phone_number VARCHAR(30),
            mail_address VARCHAR(50),
            user_point int(5),
            PRIMARY KEY(id))
            """)

con.commit()

con.close()