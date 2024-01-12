from flask import Flask, render_template, request, jsonify, redirect, session
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
from datetime import timedelta
import MySQLdb
import html
import secrets
import json

#flaskオブジェクトの作成
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=60)     

def connect():      
	con = MySQLdb.connect(
		host = "localhost",
		user = "root",
		passwd = "20030111",
		db = "super_point"
	)
	return con

con = connect()
cur = con.cursor()
cur.execute(
                    """
                    SELECT p_name, price_no_tax, price, stock_number, barcode 
                    FROM items 
                    ORDER BY c_number ASC, p_name ASC
                    """
               )
items_all=[]
for row in cur:
     items_all.append([row[0],row[1],row[2],row[3],row[4]])             
con.close()


@app.route('/count_result', methods=['POST'])
def count_result():
    content = request.form['content']
    count = str(len(content))
    count=count+" 字"
    return count

@app.route('/search_result', methods=["GET"])
def return_search_result_page():
     searchkey = request.args.get('searchkey')
     
     searchkey="%"+searchkey+"%"

     con = connect()
     cur = con.cursor()
     cur.execute(
          """
          SELECT p_name, price_no_tax, price, stock_number, barcode 
          FROM items 
          WHERE p_name LIKE %(searchkey)s 
          ORDER BY p_name DESC, stock_number DESC
          """,{"searchkey":searchkey}
     )
     
     search_result=[]
     for row in cur:
               search_result.append([row[0],row[1],row[2],row[3],row[4]])
     
     con.close()
     if searchkey != None and searchkey != '' and len(search_result) != 0:
          return render_template('search_result.html', search_result=search_result)
     else:
          return render_template('search_result.html', msg="一致なし")

@app.route("/login", methods=["GET", "POST"])
def login():
     if request.method == "GET":
          session.clear()
          return render_template("login.html",
                                 msg="メールアドレス、パスワードを入力してください：",
                                 user_admin="<a class=\"tnav tnav_hover\" href=\"/login\">" + "ログイン" + "</a>")
     elif request.method == "POST":
          user_email = request.form["user_email"]
          user_password = request.form["user_password"]
          con = connect()
          cur = con.cursor()
          cur.execute(
               """SELECT user_password,user_name,user_email,user_point,user_id,user_admin FROM users WHERE user_email=%(user_email)s""",{"user_email":user_email}
		  )
          data=[]
          for row in cur:
                data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
          if len(data)==0:
               con.close()
               return render_template("login.html", msg="メールアドレスが間違っています",
                                                    user_admin="<a class=\"tnav tnav_hover\" href=\"/login\">" + "ログイン" + "</a>")
          if cph(data[0][0], user_password):
               session["user_name"] = data[0][1]
               session["user_email"] = data[0][2]
               session["user_point"] = str(data[0][3])
               session["user_id"] = data[0][4]
               session["user_admin"] = data[0][5]
               con.close()
               return redirect("home")
          else:
               con.close()
               return render_template("login.html", msg="パスワードが間違っています",
                                                    user_admin="<a class=\"tnav tnav_hover\" href=\"/login\">" + "ログイン" + "</a>")

@app.route("/home", methods=["GET"])
def home():
    if request.method == "GET":
          if "user_name" in session:
               con = connect()
               cur = con.cursor()
               cur.execute(
                    """SELECT buy_date,buy_time,total_price FROM buy_receipts WHERE user_id=%(user_id)s ORDER BY buy_Date DESC, buy_time DESC""",{"user_id":session["user_id"]}
               )
               data=[]
               for row in cur:
                    data.append([row[0],row[1],row[2]])
               
               return render_template("index.html",
                                                  user_name=html.escape(session["user_name"]+" さん"),
                                                  user_email=html.escape(session["user_email"]),
                                                  user_point="ポイント残高："+html.escape(session["user_point"]+" pt"),
                                                  data=data,items_all=items_all,no_receipt="なし" if len(data)==0 else "",
                                                  user_admin="<a class=\"tnav tnav_hover\" href=\"/home/members\">" + session["user_name"] + " さん" + "</a>"
                                                  )
               
          else:
               return redirect("/")
          

@app.route("/home/members")
def members():
     if "user_name" in session:
          if session["user_admin"] == "admin":
               return redirect("/home/admin")
          else:
               con = connect()
               cur = con.cursor()
               cur.execute(
                    """SELECT buy_date,buy_time,total_price FROM buy_receipts WHERE user_id=%(user_id)s ORDER BY buy_Date DESC, buy_time DESC""",{"user_id":session["user_id"]}
               )
               data=[]
               for row in cur:
                    data.append([row[0],row[1],row[2]])
               
               con.commit()
               con.close()

               con = connect()
               cur = con.cursor()
               cur.execute(
                    """
                    SELECT buy_date,buy_time,total_price,payment_method,point_new,point_now,point_ticket,register_number,receipt_number
                    FROM buy_receipts 
                    WHERE user_id=%(user_id)s ORDER BY buy_Date DESC, buy_time DESC""",{"user_id":session["user_id"]}
               )
               
               receipts_all=[]
               for row in cur:
                         receipts_all.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])
               con.commit()
               con.close()

               return render_template("account.html",user_name=html.escape(session["user_name"]+" さん"),
                                                  user_email=html.escape(session["user_email"]),
                                                  user_point="ポイント残高："+html.escape(session["user_point"]+" pt"),
                                                  data=data,items_all=items_all,receipts_all=receipts_all,no_receipt="なし" if len(data)==0 else "",
                                                  user_admin="<a class=\"tnav tnav_hover\" href=\"/home/members\">" + session["user_name"] + " さん" + "</a>")
     else:
          return redirect("/login")

@app.route("/home/admin")
def admin():
     if "user_name" in session:
          if session["user_admin"] == "admin":
               con = connect()
               cur = con.cursor()
               cur.execute(
                    """SELECT users.user_email,users.user_name,customerforms.form 
                         FROM users 
                         INNER JOIN customerforms 
                         ON users.user_id = customerforms.user_id
                         ORDER BY cf_id DESC
                    """
               )
               cforms_all=[]
               for row in cur:
                    cforms_all.append([row[0],row[1],row[2]])
               
               con.commit()
               con.close()
               
               return render_template("admin.html",
                                      user_name=html.escape(session["user_name"]+" さん"),
                                      user_email=html.escape(session["user_email"]),
                                      cforms_all=cforms_all,
                                      user_admin="<a class=\"tnav tnav_hover\" href=\"/home/admin\">" + session["user_name"] + " さん" + "</a>")
          else:
               return redirect("/home/members")
     else:
          return redirect("/login")


@app.route("/")
def index():
     if "user_name" in session:
          return redirect("/home")
     else:
          return render_template("index.html",no_receipt="ログインしてください…",
                                              user_point="ポイントを見るにはログイン…",
                                              user_admin="<a class=\"tnav tnav_hover\" href=\"/login\">" + "ログイン" + "</a>",
                                              items_all=items_all)

@app.route("/logout")
def logout():
     session.clear()
     return render_template("logout.html",user_admin="<a class=\"tnav tnav_hover\" href=\"/login\">" + "ログイン" + "</a>")

@app.route('/home/customerform', methods=['GET','POST'])
def form_1():
     if "user_name" in session:
          if request.method =="GET":
               return render_template('form_1.html',
                                        user_admin="<a class=\"tnav tnav_hover\" href=\"/home/members\">" + session["user_name"] + " さん" + "</a>"
                                        )
               
          elif request.method == "POST":
               content = request.form['content']
               con = connect()
               cur = con.cursor()
               print(content)
               print(session["user_id"])
               cur.execute(
               """INSERT INTO customerforms
                         (
                         user_id,
                         form)
                         VALUES (%(user_id)s,%(content)s)
               """, {"user_id":session["user_id"],"content":content}
               )
               con.commit()
               con.close()
               return render_template('form_1_request.html',
                                      form_1_content="%s" % content,
                                      user_admin="<a class=\"tnav tnav_hover\" href=\"/home/members\">" + session["user_name"] + " さん" + "</a>"
                                      )
     else:
          return redirect("/login")

@app.route("/make", methods=["GET", "POST"])
def make():
    if request.method =="GET":
        return render_template("login_make.html",
                               user_admin="<a class=\"tnav tnav_hover\" href=\"/login\">" + "ログイン" + "</a>")
    elif request.method == "POST":
        user_pcard_number = request.form["user_pcard_number"]
        user_email = request.form["user_email"]
        user_name = request.form["user_name"]
        user_phone_number = request.form["user_phone_number"]
        user_password = request.form["user_password"]
        hashpass = gph(user_password)
        con = connect()
        cur = con.cursor()
        cur.execute(
            """SELECT * FROM users WHERE user_email=%(user_email)s
            """, {"user_email":user_email}
        )
        
        data=[]
        for row in cur:
            data.append(row)
        if len(data)!=0:
            return render_template("login_make.html", 
                                   msg="既に存在するメールアドレスです",
                                   user_admin="<a class=\"tnav tnav_hover\" href=\"/login\">" + "ログイン" + "</a>")
        con.commit()
        con.close()
        con = connect()
        cur = con.cursor()
        cur.execute(
            """INSERT INTO users
            (user_pcard_number,user_email,user_name,user_phone_number,user_password,user_point,user_point_ticket_all)
            VALUES (%(user_pcard_number)s,%(user_email)s,%(user_name)s,%(user_phone_number)s,%(hashpass)s,0,0)
            """,{"user_pcard_number":user_pcard_number, "user_email":user_email, "user_name":user_name, 
                 "user_phone_number":user_phone_number, "hashpass":hashpass}
        )
        con.commit()
        con.close()
        return render_template("login_info.html", user_pcard_number=user_pcard_number, user_email=user_email, user_name=user_name, 
                               user_phone_number=user_phone_number, user_password=user_password,
                               user_admin="<a class=\"tnav tnav_hover\" href=\"/login\">" + "ログイン" + "</a>")


#pythonで実行されたときに処理をする
if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost') 