from flask import (Flask, request, jsonify,render_template,redirect,url_for,session)
import sqlite3
import os
import psycopg2
from datetime import datetime

DEVICE_TOKEN = "ATTA_SHOP_2026_SECRET"

DATABASE = "bills.db"

def get_db_connection():
    return psycopg2.connect(
        os.environ["DATABASE_URL"]
    )

def init_db():
    # conn = sqlite3.connect(DATABASE)
    conn=get_db_connection()
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills(
        id SERIAL PRIMARY KEY,
        quantity REAL,
        rate REAL,
        amount REAL,
        created_at TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()
init_db()
app = Flask(__name__)
app.secret_key = "atta_shop_2026_super_secret_key"
@app.route("/")
def home():
    if session.get("logged_in"):
        return redirect("/menu")
        
    return redirect("/login")

@app.route("/menu")
def menu():

    if not session.get("logged_in"):
        return redirect("/login")

    return render_template("menu.html")

OWNER_PASSWORD = os.environ.get("OWNER_PASSWORD")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        password = request.form.get("password")

        if password == OWNER_PASSWORD:

            session["logged_in"] = True
            return redirect("/menu")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/billing")
def billing():
    if not session.get("logged_in"):
        return redirect("/login")
        
    return render_template("atta.html")


@app.route("/api/bill", methods=["POST"])
def save_bill():

    data = request.get_json()
    token = data.get("device_token")

    if token != DEVICE_TOKEN:
        return jsonify({
            "status": "error",
            "message": "Unauthorized"
        }), 401

    quantity = float(data["quantity"])
    rate = float(data["rate"])
    amount = float(data["amount"])

    conn = get_db_connection()
    cur=conn.cursor()

    cur.execute("""
    INSERT INTO bills(
        quantity,
        rate,
        amount,
        created_at
    )
    VALUES(%s,%s,%s,NOW())
    """,
    (
        quantity,
        rate,
        amount
    ))


    conn.commit()
    conn.close()
    print(data)
    return jsonify({
        "status": "success"
    })
    
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")
        
    conn = sqlite3.connect("bills.db")

    revenue = conn.execute(
        "SELECT IFNULL(SUM(amount),0) FROM bills"
    ).fetchone()[0]

    bill_count = conn.execute(
        "SELECT COUNT(*) FROM bills"
    ).fetchone()[0]

    total_qty = conn.execute(
        "SELECT IFNULL(SUM(quantity),0) FROM bills"
    ).fetchone()[0]

    rows = conn.execute(
        """
        SELECT *
        FROM bills
        ORDER BY id DESC
        LIMIT 20
        """
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        revenue=revenue,
        bill_count=bill_count,
        total_qty=total_qty,
        rows=rows
    )

if __name__ == "__main__":
    init_db()
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
