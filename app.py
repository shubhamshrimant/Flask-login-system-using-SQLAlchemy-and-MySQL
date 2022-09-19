# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:31:27 2022

@author: shubh
"""

from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt
engine=create_engine("mysql+pymysql://root1:XXXXXXXX@localhost/register")
#mysql+pymysql://username:password@localhost/databasename
db=scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)
app.secret_key = "RadheKrishna"

#app.static_folder = ‘static’
#register form
@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        password=request.form.get("password")
        confirm=request.form.get("confirm")
        secure_password=sha256_crypt.encrypt(str(password))
        
        usernamedata=db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        #usernamedata=str(usernamedata)
        if usernamedata==None:
            if password==confirm:
                db.execute("INSERT INTO users(name,username,password) VALUES(:name,:username,:password)",
        {"name":name,"username":username,"password":secure_password})
                db.commit()
                flash("You are registered and can now login","success")
                return redirect(url_for('login'))
            else:
                flash("password does not match","danger")
                return render_template('register.html')
        else:
            flash("user already existed, please login or contact admin","danger")
            return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        username=request.form.get("name")
        password=request.form.get("password")
        
        usernamedata=db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        passworddata=db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()
        
        if usernamedata is None:
            flash("No username","danger")
            return render_template('login.html')
        else:
            for passwor_data in passworddata:
                if sha256_crypt.verify(password,passwor_data):
                    session["log"]=True
                    
                    flash("You are now logged in!!","success")
                    return redirect(url_for('home')) #to be edited from here do redict to either svm or home
                else:
                    flash("incorrect password","danger")
                    return render_template('login.html')
    
    return render_template('login.html')

@app.route("/photo")
def photo():
    return render_template('photo.html')

@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for('login'))

@app.route("/", methods=["GET","POST"])
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)