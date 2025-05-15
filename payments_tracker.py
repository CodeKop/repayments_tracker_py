import sqlite3
from datetime import datetime, timedelta

# Database setup
DB_PATH = "car_payments.db"


def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT(250),
            start_date TEXT NOT NULL,
            initial_amount REAL NOT NULL,
            remaining_amount REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('payment', 'interest')),
            description TEXT(250),
            FOREIGN KEY (loan_id) REFERENCES loans (id)
        )
    """)
    conn.commit()
    conn.close()


def add_loan(name, date, amount, description=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    desc = description if description else None
    cursor.execute(
        "INSERT INTO loans (name, start_date, initial_amount, remaining_amount, description) VALUES (?, ?, ?, ?, ?)",
        (name, date, amount, amount, desc),
    )
    conn.commit()
    conn.close()


def add_transaction(loan_id, date, amount, transaction_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (loan_id, date, amount, type) VALUES (?, ?, ?, ?)",
        (
            loan_id,
            date.strftime("%Y-%m-%d %H:%M:%S"),
            amount,
            transaction_type,
        ),
    )
    if transaction_type == "payment":
        cursor.execute(
            "UPDATE loans SET remaining_amount = remaining_amount - ? WHERE id = ?",
            (amount, loan_id),
        )
    elif transaction_type == "interest":
        cursor.execute(
            "UPDATE loans SET remaining_amount = remaining_amount + ? WHERE id = ?",
            (amount, loan_id),
        )
    conn.commit()
    conn.close()


def calculate_interest(loan_id, rate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT remaining_amount FROM loans WHERE id = ?", (loan_id,))
    remaining_amount = cursor.fetchone()[0]
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(
        day=1
    ) - timedelta(days=1)
    daily_rate = rate / 100 / 365
    total_interest = 0

    # Calculate interest for each day in the current month
    current_date = first_day_of_month
    while current_date <= last_day_of_month:
        daily_interest = remaining_amount * daily_rate
        total_interest += daily_interest
        remaining_amount += (
            daily_interest  # Update remaining amount with daily interest
        )
        current_date += timedelta(days=1)

    # Add a single transaction for the total interest at the end of the month
    conn.close()
    # add_transaction(loan_id, total_interest, "interest")

    return loan_id, total_interest
