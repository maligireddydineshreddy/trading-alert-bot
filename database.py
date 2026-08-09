import sqlite3


DB_NAME = "alerts.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        symbol TEXT,

        target_price REAL,

        status TEXT DEFAULT 'ACTIVE'

    )
    """)


    conn.commit()

    conn.close()



def add_alert(user_id, symbol, price):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO alerts
        (user_id, symbol, target_price)

        VALUES (?, ?, ?)
        """,
        (
            user_id,
            symbol,
            price
        )
    )


    conn.commit()

    conn.close()



def get_active_alerts():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM alerts
        WHERE status='ACTIVE'
        """
    )


    alerts = cursor.fetchall()


    conn.close()


    return alerts



def disable_alert(alert_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE alerts
        SET status='DONE'
        WHERE id=?
        """,
        (alert_id,)
    )


    conn.commit()

    conn.close()