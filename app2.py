from flask import Flask, render_template, request, jsonify
import MySQLdb
import html

def connect():      
	con = MySQLdb.connect(
		host = "localhost",
		user = "root",
		passwd = "20030111",
		db = "super_point"
	)
	return con

app = Flask(__name__)

@app.route('/search')
def search():
	return render_template('search.html')

@app.route('/api/result')
def result():
	buy_date = request.args.get('buy_date')
	con = connect()
	cur = con.cursor()
	cur.execute(
		"""
		SELECT 
		receipt_id,buy_date,buy_time,receipt_number,total_price,payment_method,point_new,point_now,point_ticket
		FROM buy_receipt
		WHERE buy_date=%(buy_date)s
		""", {"buy_date" : buy_date}
	)

	res = {}
	tmpa = []
	for row in cur:
		tmpd={}
		tmpd["receipt_id"] = row[0]
		tmpd["buy_date"] = row[1]
		tmpd["buy_time"] = row[2]
		tmpd["receipt_number"] = row[3]
		tmpd["total_price"] = row[4]
		tmpd["payment_method"] = row[5]
		tmpd["point_new"] = row[6]
		tmpd["point_now"] = row[7]
		tmpd["point_ticket"] = row[8]
		tmpa.append(tmpd)
	res["receipt"] = tmpa

	return jsonify(res)

#pythonで実行されたときに処理をする
if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost') 
