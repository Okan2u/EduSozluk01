import pymongo
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# MongoDB'ye bağlantı kur

client = pymongo.MongoClient()
db = client["eduSozlukDB"]



@app.route('/hello/<name>')
def hello_name(name):
	return 'Hello %s!' % name


@app.route('/')
def home_page():
	return render_template('home.html')

@app.route('/uye_ol' , methods = ['GET' , 'POST'])
def uye_ol():
	if request.method == 'GET':
		return render_template("uye_ol.html")
	else:
		email = request.form['email']
		sifre = request.form['sifre']
		adsoyad = request.form['adsoyad']

		# Formdan gelen verileri al
		email = request.form["email"]
		sifre = request.form["sifre"]
		adsoyad = request.form["adsoyad"]

		# Verileri collection'a ekle
		db["kullanıcılar"].insert_one({
			"_id": email,
			"sifre": sifre,
			"adsoyad": adsoyad

		})

		return redirect("/",302)

@app.route('/giris' , methods = ['GET' , 'POST'])
def giris():
	if request.method == 'GET':
		return render_template("giris.html")
	else:
		email = request.form['email']
		sifre = request.form['sifre']

		kullanıcı = db["kullanıcılar"].find_one({"_id":email })
		if kullanıcı and kullanıcı["sifre"]==sifre:
			return redirect("/",302)
		else:
			return "kullanıcı bulunamadı veya şifre geçersiz"






if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0",port=5000)
