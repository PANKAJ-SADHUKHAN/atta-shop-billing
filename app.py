from flask import (Flask, request, jsonify,render_template,redirect,url_for,session,send_file)
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO
import os
import psycopg2
from datetime import datetime


def get_db_connection():
    return psycopg2.connect(
        os.environ["DATABASE_URL"]
    )

def init_db():
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

app.secret_key = os.environ.get(
    "SECRET_KEY"
)

DEVICE_TOKEN = os.environ.get(
    "DEVICE_TOKEN"
)

OWNER_PASSWORD = os.environ.get("OWNER_PASSWORD")

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

    try:

        if not session.get("logged_in"):
            return jsonify({
                "error": "Unauthorized"
            }), 401

        data = request.get_json()

        print("Received:", data)

        if data.get("device_token") != DEVICE_TOKEN:
            return jsonify({
                "error": "Invalid Device"
            }), 403

        quantity = float(data["quantity"])

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO bills(
                quantity,
                created_at
            )
            VALUES(%s, NOW())
            RETURNING id
        """, (quantity,))
        bill_id = cur.fetchone()[0]

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "status": "success",
            "bill_id": bill_id
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/delete-bill/<int:bill_id>",
           methods=["POST"])
def delete_bill(bill_id):

    if not session.get("logged_in"):
        return jsonify({
            "error": "Unauthorized"
        }), 401

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM bills
        WHERE id = %s
        """,
        (bill_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Bill Deleted"
    })
    
@app.route("/download-pdf")
def download_pdf():

    if not session.get("logged_in"):
        return redirect("/login")

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT quantity, created_at
        FROM bills
        WHERE DATE(created_at)
        BETWEEN %s AND %s
        ORDER BY created_at
    """, (from_date, to_date))

    rows = cur.fetchall()

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(pdf_buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Sadhukhan Enterprise Sales Report",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            f"From: {from_date} To: {to_date}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 12))

    total_qty = 0

    for row in rows:

        qty = row[0]

        total_qty += qty

        elements.append(
            Paragraph(
                f"{row[1]} - {qty} Kg",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Total Bills: {len(rows)}",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Total Quantity: {total_qty} Kg",
            styles["Heading2"]
        )
    )

    doc.build(elements)

    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="sales_report.pdf",
        mimetype="application/pdf"
    )

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")
        
    conn = get_db_connection()
    cur=conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM bills
        WHERE DATE(created_at)=CURRENT_DATE
    """)
    bill_count = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(SUM(quantity),0)
        FROM bills
        WHERE DATE(created_at)=CURRENT_DATE
    """)
    total_qty = cur.fetchone()[0]

    cur.execute("""
        SELECT *
        FROM bills
        WHERE DATE(created_at)=CURRENT_DATE
        ORDER BY id DESC
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        bill_count=bill_count,
        total_qty=total_qty,
        rows=rows
    )
    

if __name__ == "__main__":
    init_db()
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
