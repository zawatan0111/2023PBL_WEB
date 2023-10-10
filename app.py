from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html',  title="ポイントカード照会ページ",  message="ポイントカード番号を入力")

@app.route('/', methods=['POST'])
def   form():
	field = request.form['field']
	return render_template('index.html', title="%s さんのポイントカード照会ページ" % field,  message="保有ポイント : ")

if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost') 