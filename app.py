
from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret-key"

db = mysql.connector.connect(
    host="db4free.net",
    user="caiishly_user",
    password="Aa112233@",
    database="caiishly_db"
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user'] = username
            return redirect('/dashboard')
        else:
            flash("اسم المستخدم أو كلمة المرور غير صحيحة")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html', user=session['user'])

@app.route('/add', methods=['GET', 'POST'])
def add_transfer():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        customer = request.form['customer']
        merchant = request.form['merchant']
        amount = request.form['amount']
        currency = request.form['currency']
        phone = request.form['phone']
        notes = request.form['notes']
        status = request.form['status']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO transfers (customer_name, merchant_name, date, amount, currency, phone, notes, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (customer, merchant, date, amount, currency, phone, notes, status))
        db.commit()
        flash("تم حفظ الحوالة")
        return redirect('/dashboard')
    return render_template('add_transfer.html')

if __name__ == '__main__':
    app.run(debug=True)
