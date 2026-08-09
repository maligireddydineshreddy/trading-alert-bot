import sqlite3


DB_NAME = "alerts.db"





# ==========================
# CREATE DATABASE
# ==========================


def init_db():


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        symbol TEXT,

        target_price REAL,

        direction TEXT,

        status TEXT DEFAULT 'ACTIVE'

    )
    """)



    conn.commit()

    conn.close()







# ==========================
# ADD ALERT
# ==========================


def add_alert(user_id, symbol, price, direction):


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()



    cursor.execute(
        """
        INSERT INTO alerts
        (
            user_id,
            symbol,
            target_price,
            direction
        )

        VALUES (?, ?, ?, ?)

        """,

        (
            user_id,
            symbol,
            price,
            direction
        )

    )



    conn.commit()

    conn.close()







# ==========================
# USER ALERTS
# ==========================


def get_user_alerts(user_id):


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT *
        FROM alerts

        WHERE user_id=?

        AND status='ACTIVE'

        """,

        (user_id,)

    )



    alerts = cursor.fetchall()



    conn.close()



    return alerts







# ==========================
# ALL ACTIVE ALERTS
# ==========================


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







# ==========================
# REMOVE ALERT
# ==========================


def remove_alert(alert_id):


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







# ==========================
# DISABLE AFTER HIT
# ==========================


def disable_alert(alert_id):

    remove_alert(alert_id)
