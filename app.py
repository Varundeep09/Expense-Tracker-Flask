from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
import os
from datetime import datetime, timedelta
import csv
from io import StringIO
from collections import defaultdict
import calendar
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# MySQL Connection Setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_tracker",
        
    )


from werkzeug.security import generate_password_hash, check_password_hash

# def hash_password(password):
#     return generate_password_hash(password)

# def check_password(password, hashed):
#     return check_password_hash(hashed, password)


# Utility Functions
def get_monthly_expenses(user_id, year=None, month=None):
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month

    start_date = datetime(year, month, 1).date()
    end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1) if month == 12 else datetime(year, month + 1, 1).date() - timedelta(days=1)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        'SELECT * FROM expenses WHERE user_id = %s AND date >= %s AND date <= %s ORDER BY date DESC',
        (user_id, start_date, end_date)
    )
    expenses = cursor.fetchall()
    conn.close()

    for expense in expenses:
        expense['date'] = expense['date'] if isinstance(expense['date'], datetime) else datetime.strptime(str(expense['date']), '%Y-%m-%d').date()

    return expenses


def calculate_spending_forecast(expenses, monthly_budget):
    monthly_budget = float(monthly_budget)  # Already float now
    now = datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    days_passed = now.day
    days_left = days_in_month - days_passed

    current_spending = sum(float(expense['amount']) for expense in expenses)

    if days_passed == 0:
        return {
            'predicted_total': 0,
            'current_spending': current_spending,
            'days_left': days_left,
            'risk_level': 'low',
            'recommendations': [],
            'daily_average': 0
        }

    daily_average = current_spending / days_passed

    recent_date = now.date() - timedelta(days=min(7, days_passed))
    recent_expenses = [e for e in expenses if e['date'] >= recent_date]
    recent_total = sum(float(expense['amount']) for expense in recent_expenses)
    recent_days = min(7, days_passed)
    recent_daily_average = recent_total / recent_days if recent_days > 0 else daily_average

    weighted_daily_average = (recent_daily_average * 0.6) + (daily_average * 0.4)
    predicted_total = current_spending + (weighted_daily_average * days_left)

    if monthly_budget > 0:
        spending_percentage = (predicted_total / monthly_budget) * 100
        if spending_percentage >= 100:
            risk_level = 'high'
        elif spending_percentage >= 80:
            risk_level = 'medium'
        else:
            risk_level = 'low'
    else:
        risk_level = 'low'

    recommendations = generate_recommendations(expenses, risk_level, weighted_daily_average)

    return {
        'predicted_total': predicted_total,
        'current_spending': current_spending,
        'days_left': days_left,
        'risk_level': risk_level,
        'recommendations': recommendations,
        'daily_average': weighted_daily_average
    }

def generate_recommendations(expenses, risk_level, daily_average):
    recommendations = []

    if risk_level == 'low':
        recommendations.append("Great job! You're on track with your spending.")
        recommendations.append('Consider setting aside extra money for savings.')
        return recommendations

    category_spending = defaultdict(float)
    for expense in expenses:
        category_spending[expense['category']] += float(expense['amount'])  # FIX: convert Decimal to float

    total_spending = sum(category_spending.values())
    sorted_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:3]

    if risk_level == 'medium':
        recommendations.append("You're spending above your usual rate. Consider these adjustments:")
    else:
        recommendations.append('⚠️ High spending alert! Take immediate action:')

    for category, amount in sorted_categories:
        percentage = (amount / total_spending) * 100 if total_spending > 0 else 0

        if category == 'food' and percentage > 30:
            recommendations.append(f'🍽️ Food expenses are {percentage:.0f}% of spending. Try meal planning and cooking at home.')
        elif category == 'entertainment' and percentage > 20:
            recommendations.append(f'🎬 Entertainment is {percentage:.0f}% of spending. Consider free activities.')
        elif category == 'shopping' and percentage > 25:
            recommendations.append(f'🛍️ Shopping expenses are high at {percentage:.0f}%. Wait 24 hours before purchases.')
        elif category == 'transport' and percentage > 20:
            recommendations.append(f'🚗 Transport costs are {percentage:.0f}% of spending. Consider public transport.')

    if daily_average > 50:
        recommendations.append('💡 Try the "24-hour rule" - wait a day before purchases over ₹100.')

    return recommendations


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        monthly_budget = request.form.get("monthly_budget", 0.0)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, monthly_budget) VALUES (%s, %s, %s, %s)",
            (name, email, password, monthly_budget)
        )
        conn.commit()
        conn.close()
        print("✅ User registered successfully")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(f"[DEBUG] Login Attempt: {email}, password: {password}")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            print(f"[DEBUG] Found user: {user['email']}, checking password...")
            print(f"[DEBUG] Input Password: {password}")
            print(f"[DEBUG] Stored Password: {user['password_hash']}")

            if password == user["password_hash"]:
                session["user_id"] = user["id"]
                session["user_email"] = user["email"]
                print("✅ Login successful")
                return redirect(url_for("dashboard"))
            else:
                print("❌ Login failed: Incorrect password")
                return render_template("login.html", error="Invalid credentials")
        else:
            print("❌ Login failed: Email not found")
            return render_template("login.html", error="User not found")

    return render_template("login.html")




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    user['monthly_budget'] = float(user['monthly_budget'])  # ✅ Convert Decimal to float
    conn.close()

    if not user:
        flash("User not found. Please log in again.", "error")
        return redirect(url_for('logout'))  # clear session safely

    expenses = get_monthly_expenses(user_id)
    # FIX: Pass monthly_budget as float here
    forecast = calculate_spending_forecast(expenses, float(user['monthly_budget']))

    category_data = defaultdict(float)
    for expense in expenses:
        category_data[expense['category']] += float(expense['amount'])  # FIXED convert Decimal to float

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM expenses WHERE user_id = %s ORDER BY created_at DESC LIMIT 5', (user_id,))
    recent_expenses = cursor.fetchall()
    conn.close()

    for expense in recent_expenses:
        expense['date'] = expense['date'] if isinstance(expense['date'], datetime) else datetime.strptime(str(expense['date']), '%Y-%m-%d').date()

    return render_template('dashboard.html',
                           expenses=expenses,
                           forecast=forecast,
                           category_data=dict(category_data),
                           recent_expenses=recent_expenses,
                           user=user)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        # Save the expense to DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (user_id, amount, category, description, date, is_recurring, recurring_frequency)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            user_id,
            float(request.form['amount']),
            request.form['category'],
            request.form['description'],
            request.form['date'],
            1 if request.form.get('is_recurring') else 0,
            request.form.get('recurring_frequency') if request.form.get('is_recurring') else None
        ))
        conn.commit()
        conn.close()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))

    # For GET request or if you want to render the form after POST failure:
    # Fetch user and expenses to calculate forecast
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    conn.close()

    expenses = get_monthly_expenses(user_id)
    forecast = calculate_spending_forecast(expenses, float(user['monthly_budget']))

    return render_template('add_expense.html', forecast=forecast, user=user)


@app.route('/expenses')
def expenses():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        'SELECT * FROM expenses WHERE user_id = %s ORDER BY date DESC LIMIT %s OFFSET %s',
        (session['user_id'], per_page, offset)
    )
    expenses = cursor.fetchall()

    cursor.execute(
        'SELECT COUNT(*) AS total FROM expenses WHERE user_id = %s',
        (session['user_id'],)
    )
    total = cursor.fetchone()['total']

    conn.close()

    # Convert dates to proper format
    converted_expenses = []
    for expense in expenses:
        expense['date'] = expense['date'] if isinstance(expense['date'], datetime) else datetime.strptime(str(expense['date']), '%Y-%m-%d').date()
        converted_expenses.append(expense)

    # Simple pagination object
    class Pagination:
        def __init__(self, page, per_page, total):
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page
            self.has_prev = page > 1
            self.has_next = page < self.pages
            self.prev_num = page - 1 if self.has_prev else None
            self.next_num = page + 1 if self.has_next else None
            self.items = []

    pagination = Pagination(page, per_page, total)
    pagination.items = converted_expenses

    return render_template('expenses.html', expenses=pagination)

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET monthly_budget = %s, alert_threshold = %s WHERE id = %s',
            (float(request.form['monthly_budget']), float(request.form['alert_threshold']), user_id)
        )
        conn.commit()
        conn.close()

        flash('Budget settings updated!', 'success')
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    conn.close()

    return render_template('budget.html', user=user)

@app.route('/export_csv')
def export_csv():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    month = request.args.get('month', datetime.now().month, type=int)
    year = request.args.get('year', datetime.now().year, type=int)

    expenses = get_monthly_expenses(session['user_id'], year, month)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Category', 'Description', 'Amount', 'Recurring'])

    for expense in expenses:
        writer.writerow([
            expense['date'].strftime('%Y-%m-%d'),  # convert date object to string
            expense['category'],
            expense['description'],
            expense['amount'],
            'Yes' if expense['is_recurring'] else 'No'
        ])

    output.seek(0)

    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=expenses_{year}_{month:02d}.csv'

    return response

@app.route('/api/chart_data')
def chart_data():
    if 'user_id' not in session:
        return jsonify({})

    expenses = get_monthly_expenses(session['user_id'])
    category_data = defaultdict(float)

    for expense in expenses:
        category_data[expense['category']] += float(expense['amount'])  # FIX: convert Decimal to float

    return jsonify(dict(category_data))

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM expenses WHERE id = %s AND user_id = %s', (expense_id, user_id))
    expense = cursor.fetchone()
    if not expense:
        conn.close()
        flash('Expense not found or unauthorized action.', 'error')
        return redirect(url_for('expenses'))

    cursor.execute('DELETE FROM expenses WHERE id = %s', (expense_id,))
    conn.commit()
    conn.close()
    flash('Expense deleted successfully.', 'success')
    return redirect(url_for('expenses'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
