ExpenseWise - Smart Expense Tracker


A comprehensive Flask-based expense tracking web application featuring intelligent budgeting, spending forecasts, and personalized financial insights.

Features
Core Functionality
User Authentication: Secure login and registration with password hashing and session management

Expense Tracking: Add, view, and categorize daily expenses with detailed descriptions and dates

Smart Dashboard: Intuitive interface showing spending analytics, budget usage, and recent transactions

Budget Management: Set monthly budgets with customizable alert thresholds

Advanced Features
Budget Forecasting: Spending predictions based on weighted averages of recent and monthly trends

Overspend Alerts: Real-time warnings with personalized recommendations to control expenses

Visual Analytics: Interactive pie charts illustrating spending breakdown by category

Recurring Expenses: Support for tracking recurring payments and subscriptions

CSV Export: Download monthly expense reports in CSV format for offline analysis

Responsive Design: Mobile-friendly UI that adapts to all device sizes

Installation
Prerequisites
Python 3.8 or higher

MySQL 5.7 or higher (or compatible MariaDB)

pip (Python package manager)

Setup Instructions
Clone the repository

bash
Copy
Edit
git clone <repository-url>
cd expense-tracker
Create and activate a virtual environment

bash
Copy
Edit
python -m venv venv
# On Linux/macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate
Install required Python packages

bash
Copy
Edit
pip install -r requirements.txt
Database Setup

Create a MySQL database named expense_tracker

Execute the SQL schema script to create necessary tables:

bash
Copy
Edit
mysql -u your_mysql_user -p expense_tracker < database_setup.sql
Update the database credentials in your app.py connection function if necessary

Run the application

bash
Copy
Edit
python app.py
Access the app
Open your browser and navigate to http://localhost:5000

Usage
Register an account with your email and set your monthly budget

Add expenses with detailed categories, amounts, descriptions, and dates

Monitor your spending and budget forecasts on the dashboard

Receive alerts if you approach or exceed your budget

Export monthly expense data as CSV files for record-keeping

Categories
🍽️ Food & Dining

🚗 Transportation

🎬 Entertainment

🛍️ Shopping

📋 Bills & Utilities

🏥 Healthcare

🎓 Education

✈️ Travel

🏷️ Other

Technical Stack
Backend: Flask (Python web framework)

Database: MySQL (using mysql-connector-python)

Frontend: HTML5, CSS3, JavaScript

Charts: Chart.js for interactive data visualization

Security: Password hashing with SHA-256, session management, CSRF protection via Flask

Security Considerations
Passwords hashed securely before storage

SQL queries use parameterized statements to prevent SQL injection

Session-based authentication for user access control

Input validation and sanitization on forms

Contributing
Contributions are welcome! Please fork the repository and create feature branches for new work.

Fork the repo

Create a new branch: git checkout -b feature/your-feature-name

Commit your changes: git commit -m "Add feature"

Push the branch: git push origin feature/your-feature-name

Open a Pull Request

License
This project is licensed under the MIT License. See the LICENSE file for details.

Support
For any issues or feature requests, please open an issue in the GitHub repository.

ExpenseWise — Empower your financial health with smart tracking and insightful analytics.