from flask import Flask,render_template,request, session, url_for, escape, redirect, abort, make_response
import googlemaps
import key
import json
import use_csv
import string
import random
from werkzeug.utils import secure_filename
import os
import db
import genpass
import otp_gen

pyBot = db.Database()

csvData = use_csv.Data()

api_key = key.key

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app=Flask(__name__)
app.secret_key = "teamblu"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
req_image = os.path.join('static', 'img')

def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    x = ''.join(random.choice(chars) for _ in range(size))
    return x

def otp_generator(size=4, chars=string.digits):
    otp = ''.join(random.choice(chars) for _ in range(size))
    return otp

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET"])
def geoloc():
	gmaps = googlemaps.Client(key=api_key)
	loc = gmaps.geolocate()
	locations = csvData.read_data(loc)
	pre_lat = loc['location']['lat']
	pre_lng = loc['location']['lng']
	return render_template("testmap.html", session=session, api_key=api_key, pre_lat = pre_lat, pre_lng=pre_lng,loc=loc,locations=locations)

@app.route('/request')
def send_loc():
	gmaps = googlemaps.Client(key=api_key)
	loc = gmaps.geolocate()
	pre_lat = loc["location"]["lat"]
	pre_lng = loc["location"]["lng"]
	un_id = id_generator()
	return render_template("request.html", pre_lat=pre_lat, pre_lng=pre_lng, un_id=un_id)

@app.route('/requestsent', methods=["POST"])
def loc_received():
	pre_lat = request.form["getlat"]
	pre_lng = request.form["getlng"]
	file = request.files['file']
	un_id = request.form["unid"]
	user = session["mobile"]
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], un_id+".jpg"))

	sent_data = csvData.write_data(un_id, pre_lat, pre_lng, user)
	otp_gen.new_request(user, un_id)
	return render_template("datasent.html", un_id = un_id)

@app.route('/login')
def log_in():
	if 'username' in session:
		session['login'] = "signed_in"
		return redirect(url_for('geoloc'))
	return render_template("login.html")

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/otpconfirm', methods=["POST"])
def otpconfirm():
	session["mobile"] = request.form["userid"]
	session["password"] = request.form["user_pass"]
	otp = otp_generator()
	session["otp"] = otp
	try:
		otp_gen.sendsms(session["mobile"], otp)
		return render_template("otpsent.html")
	except:
		return render_template("registration_error.html")

@app.route('/registrationconfirm', methods=["POST"])
def registration():
	if request.form["user_otp"] == session["otp"]:
		session.pop('otp', None)
		mobile = session["mobile"]
		password = session["password"]
		try:
			pyBot.register_user(mobile, password)
			return render_template("success.html")
		except:
			return render_template("registration_error.html")
	else:
		render_template("registration_error.html")

@app.route('/validate', methods=["POST"])
def validate():
	uid = request.form["userid"]
	upass = request.form["user_pass"]
	check_user = pyBot.con_auth(uid, upass)
	if check_user == None:
		return render_template("nouser.html")
	else:
		session['mobile'] = uid
		session['login'] = "signed_in"
		session['usertype'] = check_user['usertype']
		print(session)
		return redirect(url_for('geoloc'))

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('login', None)
	session.pop('usertype', None)
	return redirect(url_for('geoloc'))
		
@app.route('/dashboard', methods=["GET"])
def dashboard():
	if session["usertype"] != "admin":
		abort(404)
	else:
		get_locations = csvData.read_data("csv")
		img_path = []
		for loc in get_locations:
			loc_file = loc[0]+".jpg"
			for files in os.walk(req_image):
				if loc_file in files[2]:
					path = os.path.join(req_image, loc_file)
					img_path.append(path)

		return render_template('dashboard.html', img_path=img_path, locations=get_locations)
	return make_response("Connected", 200)

@app.route('/closedrequests', methods=["GET"])
def closedrequests():
	if session["usertype"] != "admin":
		abort(404)
	else:
		get_locations = csvData.closed_data("csv")
		img_path = []
		for loc in get_locations:
			loc_file = loc[0]+".jpg"
			for files in os.walk(req_image):
				if loc_file in files[2]:
					path = os.path.join(req_image, loc_file)
					img_path.append(path)

		return render_template('closedrequests.html', img_path=img_path, locations=get_locations)
	return make_response("Connected", 200)

@app.route('/closerequest', methods=["POST"])
def closerequest():
	unique_id = request.form["un_id"]
	return render_template("close.html", unique_id=unique_id)

@app.route('/closed', methods=["POST"])
def closed():
	unique_id = request.form["un_id"]
	csvData.change_value(unique_id)
	return redirect("/dashboard")

@app.route('/adminregister')
def adminregister():
	return render_template('adminregister.html')

@app.route('/adminregistered', methods=["POST"])
def adminregistered():
	adminID = request.form["userid"]
	adminPass = request.form["user_pass"]
	try:
		pyBot.register_admin(adminID, adminPass)
		return render_template("success.html")
	except:
		return render_template("registration_error.html")

if __name__=='__main__':
	app.run(debug=True, host="127.0.0.1")
