
from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "sharma_advanced_secret"

def db():
    conn = sqlite3.connect("garage.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/services")
def services():
    conn = db()
    data = conn.execute("SELECT * FROM services").fetchall()
    conn.close()
    return render_template("services.html", services=data)

@app.route("/book", methods=["GET","POST"])
def book():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        car = request.form["car"]
        service = request.form["service"]

        conn = db()
        conn.execute("INSERT INTO bookings(name,phone,car,service) VALUES(?,?,?,?)",
                     (name,phone,car,service))
        conn.commit()
        conn.close()

        return render_template("success.html")

    return render_template("book.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == "admin" and pwd == "admin":
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")

@app.route("/admin", methods=["GET","POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = db()

    if request.method == "POST":
        service = request.form["service"]
        price = request.form["price"]
        conn.execute("INSERT INTO services(service,price) VALUES(?,?)",(service,price))
        conn.commit()

    services = conn.execute("SELECT * FROM services").fetchall()
    bookings = conn.execute("SELECT * FROM bookings").fetchall()
    conn.close()

    return render_template("admin.html", services=services, bookings=bookings)

@app.route("/invoice", methods=["POST"])
def invoice():
    name = request.form["name"]
    service = request.form["service"]
    amount = request.form["amount"]
    gst = float(amount) * 0.18
    total = float(amount) + gst

    file = "gst_invoice.pdf"
    c = canvas.Canvas(file)

    c.drawString(100,750,"Sharma Motor Works - GST Invoice")
    c.drawString(100,720,f"Customer: {name}")
    c.drawString(100,690,f"Service: {service}")
    c.drawString(100,660,f"Amount: Rs {amount}")
    c.drawString(100,630,f"GST (18%): Rs {gst}")
    c.drawString(100,600,f"Total: Rs {total}")

    c.save()

    return send_file(file, as_attachment=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    apprun(host="0.0.0.0", port=port)
