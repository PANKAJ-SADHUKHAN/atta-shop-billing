from flask import Flask, request, jsonify,render_template
import sqlite3
from datetime import datetime



DATABASE = "bills.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS bills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quantity REAL,
        rate REAL,
        amount REAL,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()
init_db()
app = Flask(__name__)
@app.route("/")
def home():
    return """
    <h2>Atta Shop System</h2>

    <a href='/billing'>Billing Page</a><br><br>

    <a href='/dashboard'>Dashboard</a>
    """
@app.route("/billing")
def billing():
    return render_template("atta_billing.html")


@app.route("/api/bill", methods=["POST"])
def save_bill():

    print("API HIT")
    data = request.get_json()

    quantity = float(data["quantity"])
    rate = float(data["rate"])
    amount = float(data["amount"])

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
    INSERT INTO bills(
        quantity,
        rate,
        amount,
        created_at
    )
    VALUES(?,?,?,?)
    """,
    (
        quantity,
        rate,
        amount,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))


    conn.commit()
    conn.close()
    print(data)
    return jsonify({
        "status": "success"
    })
    
@app.route("/dashboard")
def dashboard():

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
