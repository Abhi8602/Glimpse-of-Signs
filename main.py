from flask import Flask,render_template,request,send_file
from connection_ import *
import json,random,smtplib,io

app = Flask(__name__)    

@app.route('/')
def main():
    return render_template('index.html')

@app.route("/home", methods = ["GET", "POST"])
def home_():
    if request.method == "POST":
        data = request.form
        if data["name"] == "" or data["email"] == "" or data["password"] == "" or data["dob"] == "":
            return render_template("home.html",msg=True)
        else:
            insert_user(data["name"],data["email"],data["password"],data["dob"])
            return render_template("login.html",msg = False)
    return render_template("home.html",msg = False)

@app.route("/login", methods = ["GET", "POST"])
def login_():
    if request.method == "POST":
        data = request.form
        if data["password"] == verify_pass(data["email"]):
            if status(data["email"]) =="user":
                id = get_id(data["email"])
                zodiac = get_zodiac(get_db(id))
                login_times(data["email"])
                with open("info.json","r") as data_file:
                    data = json.load(data_file)
                data = data[zodiac.title()]
                return render_template("template.html",zodiac = zodiac,data = data)
            else:
                login_times(data["email"])
                data = user_info.find()
                return render_template('admin.html', data = data)
        return render_template("login.html",msg = True)
    return render_template("login.html",msg = False)

@app.route('/aboutus')
def about_us():
    return render_template('index.html')

@app.route('/contact')
def contact_():
    return render_template('index.html')

@app.route('/forgotpassword', methods = ["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        data = request.form
        email_=email_verify(data["email"])
        if data["email"] ==email_:
            my_email="tp753855@gmail.com"
            password="lwrvnzjjvrrvcdrf"
            global number_otp
            global emailtochange
            conn=smtplib.SMTP("smtp.gmail.com", port=587)
            emailtochange = email_
            number_otp = otp()
            conn.starttls()
            conn.login(user=my_email,password=password)
            conn.sendmail(from_addr=my_email,to_addrs=email_,msg="Subject:Forgot Password\n\n"+number_otp)
            conn.close()
            return render_template("changepassword.html",email=data["email"],msg=False)
        else:
            return render_template("forgotpassword.html",msg=True)
    return render_template("forgotpassword.html",msg=False)


@app.route('/changepassword', methods = ["GET", "POST"])
def change_password():
    if request.method == "POST":
        data = request.form
        if data["code"]==number_otp:
            update_pass_(emailtochange,data["password"])
            return render_template('login.html',msg=False)
    return render_template('changepassword.html',msg=True,email=emailtochange)
    
@app.route('/admin')
def plot_png():
    fig = show_signs()
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
    return send_file(output, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug = True)