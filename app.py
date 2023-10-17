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
    return render_template('form_1_request.html')


@app.route('/price')
def price():
    return render_template('price.html')

#pythonで実行されたときに処理をする
if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost') 

