import sqlite3
from datetime import datetime


DATABASE_NAME = "customer_feedback.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Customer table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            created_date TEXT NOT NULL
        )
    """)

    # Feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            review TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            sentiment_score REAL,
            rating TEXT,
            feedback_date TEXT NOT NULL,

            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
        )
    """)

    connection.commit()
    connection.close()


def save_customer(
    customer_id,
    name,
    email=None,
    phone=None
):
    connection = get_connection()
    cursor = connection.cursor()

    # Check whether customer already exists
    cursor.execute("""
        SELECT customer_id, name, email, phone
        FROM customers
        WHERE customer_id = ?
    """, (customer_id,))

    existing_customer = cursor.fetchone()

    if existing_customer:

        old_name = existing_customer[1]
        old_email = existing_customer[2]
        old_phone = existing_customer[3]

        # Keep old information if new value is empty
        updated_name = name if name else old_name
        updated_email = email if email else old_email
        updated_phone = phone if phone else old_phone

        cursor.execute("""
            UPDATE customers
            SET name = ?,
                email = ?,
                phone = ?
            WHERE customer_id = ?
        """, (
            updated_name,
            updated_email,
            updated_phone,
            customer_id
        ))

    else:

        cursor.execute("""
            INSERT INTO customers
            (
                customer_id,
                name,
                email,
                phone,
                created_date
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer_id,
            name,
            email,
            phone,
            datetime.now().strftime("%Y-%m-%d")
        ))

    connection.commit()
    connection.close()


def save_feedback(
    customer_id,
    review,
    sentiment,
    sentiment_score,
    rating=None
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback
        (
            customer_id,
            review,
            sentiment,
            sentiment_score,
            rating,
            feedback_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        customer_id,
        review,
        sentiment,
        sentiment_score,
        rating,
        datetime.now().strftime("%Y-%m-%d")
    ))

    connection.commit()
    connection.close()


# ---------------------------------
# Customer History
# ---------------------------------

def get_customer_history(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            feedback_id,
            review,
            sentiment,
            sentiment_score,
            rating,
            feedback_date
        FROM feedback
        WHERE customer_id = ?
        ORDER BY feedback_id ASC
    """, (customer_id,))

    history = cursor.fetchall()

    connection.close()

    return history


# ---------------------------------
# Feedback Summary
# ---------------------------------

def get_feedback_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_feedback,

            SUM(
                CASE
                    WHEN sentiment = 'Positive'
                    THEN 1
                    ELSE 0
                END
            ),

            SUM(
                CASE
                    WHEN sentiment = 'Negative'
                    THEN 1
                    ELSE 0
                END
            ),

            SUM(
                CASE
                    WHEN sentiment = 'Neutral'
                    THEN 1
                    ELSE 0
                END
            )

        FROM feedback
    """)

    summary = cursor.fetchone()

    connection.close()

    return summary


# ---------------------------------
# Total Customers
# ---------------------------------

def get_total_customers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
    """)

    total_customers = cursor.fetchone()[0]

    connection.close()

    return total_customers


# ---------------------------------
# All Customers
# ---------------------------------

def get_all_customers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            customer_id,
            name,
            email,
            phone,
            created_date
        FROM customers
        ORDER BY created_date DESC
    """)

    customers = cursor.fetchall()

    connection.close()

    return customers


# ---------------------------------
# Customer Details
# ---------------------------------

def get_customer_details(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            customer_id,
            name,
            email,
            phone,
            created_date
        FROM customers
        WHERE customer_id = ?
    """, (customer_id,))

    customer = cursor.fetchone()

    connection.close()

    return customer


# ---------------------------------
# All Feedback
# ---------------------------------

def get_all_feedback():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            f.feedback_id,
            f.customer_id,
            c.name,
            f.review,
            f.sentiment,
            f.sentiment_score,
            f.rating,
            f.feedback_date

        FROM feedback f

        LEFT JOIN customers c
        ON f.customer_id = c.customer_id

        ORDER BY f.feedback_id DESC
    """)

    feedback = cursor.fetchall()

    connection.close()

    return feedback


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")