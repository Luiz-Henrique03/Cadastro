import sqlite3
from flask import Flask,render_template,request,redirect
import os
from flask_mail import Mail,Message

app = Flask(__name__)


SPORTS = ["Futebol","Volei","Basquete","Ping Pong"]

@app.route("/",methods=["POST","GET"])
def index():
         return render_template("index.html", sports=SPORTS)

@app.route("/register",methods=["POST","GET"])
def register():
    con = sqlite3.connect("cadastros.db")
    cur = con.cursor()
    cur.execute('create table if not exists registrants( id integer, name text not null,' \
                ' sport text not null,primary key(id))')
    email = request.form.get("email")
    if not email:
        return render_template("error.html",message="Dont have a name")
    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html",message="Dont have a sport")
    if sport not in SPORTS:
        return render_template("error.html",message="Dont have a valid sport")

    cur.execute("INSERT INTO registrants(name,sport) VALUES(?,?)",(email,sport))
    con.commit()

    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    con = sqlite3.connect("cadastros.db")
    cur = con.cursor()
    registrants = cur.execute("SELECT * FROM registrants")
    return render_template("registrants.html",registrants=registrants)

