# Atta Billing System

A lightweight billing and sales management web application developed for an atta (flour) shop.

## Features

* Secure login system
* Generate atta sales receipts
* Thermal printer support (58mm Bluetooth thermal printer)
* Automatic bill numbering
* PostgreSQL database storage
* Dashboard for sales tracking
* Delete incorrect bills
* PDF report generation by date range
* Progressive Web App (PWA) support
* Mobile-friendly responsive design

---

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Flask (Python)

### Database

* PostgreSQL

### Hosting

* Render

### Reporting

* ReportLab (PDF Generation)

---

## Project Structure

```text
atta-billing/
│
├── app.py
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── menu.html
│   ├── atta.html
│   └── dashboard.html
│
├── static/
│   ├── manifest.json
│   ├── sw.js
│   ├── icon-192.png
│   └── icon-512.png
│
└── README.md
```

---

## Main Functionalities

### Login

Shop owner authentication using a password stored in Render Environment Variables.

### Billing

* Enter atta quantity
* Generate receipt
* Save bill into PostgreSQL
* Generate unique bill number

### Dashboard

Displays:

* Total bills
* Total atta sold
* Recent sales

Allows:

* Delete incorrect bills

### PDF Report

Generate sales reports for a selected date range.

---

## Environment Variables

Create the following environment variables in Render:

```env
DATABASE_URL=your_postgresql_connection_string
OWNER_PASSWORD=your_password
SECRET_KEY=your_secret_key
DEVICE_TOKEN=your_device_token
```

---

## Database Schema

```sql
CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    quantity REAL,
    rate REAL,
    amount REAL,
    created_at TIMESTAMP
);
```

---

## Thermal Printing

Tested with:

* BT-58 Bluetooth Thermal Printer
* RawBT Android Printing Service

Receipt includes:

* Bill Number
* Shop Details
* Date & Time
* Quantity Sold

---

## Future Improvements

* Native Android Application
* Direct Bluetooth Printing (without RawBT)
* Customer Database
* Multiple Product Support
* Inventory Management
* Push Notifications

---

## Author

Pankaj Sadhukhan

Developed as a practical billing solution for a local atta shop while learning Flask, PostgreSQL, Render deployment, Progressive Web Apps, and thermal printer integration.
