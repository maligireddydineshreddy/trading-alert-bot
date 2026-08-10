import sqlite3
import os


DB_NAME = "/app/data/alerts.db"





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

        direction TEXT DEFAULT 'ABOVE',

        status TEXT DEFAULT 'ACTIVE'

    )
    """)



    # ==========================
    # DATABASE MIGRATION
    # ==========================


    cursor.execute(
        "PRAGMA table_info(alerts)"
    )


    columns = [

        row[1]

        for row in cursor.fetchall()

    ]



    if "direction" not in columns:


        cursor.execute(
            """
            ALTER TABLE alerts

            ADD COLUMN direction TEXT DEFAULT 'ABOVE'

            """
        )



    if "status" not in columns:


        cursor.execute(
            """
            ALTER TABLE alerts

            ADD COLUMN status TEXT DEFAULT 'ACTIVE'

            """
        )



    conn.commit()

    conn.close()







# ==========================
# ADD ALERT
# ==========================


def add_alert(
    user_id,
    symbol,
    price,
    direction
):


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
# GET USER ACTIVE ALERTS
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

        ORDER BY id DESC

        """,

        (
            user_id,
        )

    )



    alerts = cursor.fetchall()



    conn.close()



    return alerts







# ==========================
# GET ALL ACTIVE ALERTS
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
# REMOVE SINGLE ALERT
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

        (
            alert_id,
        )

    )



    conn.commit()

    conn.close()







# ==========================
# REMOVE MULTIPLE ALERTS
# ==========================


def remove_multiple_alerts(alert_ids):


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()



    for alert_id in alert_ids:


        cursor.execute(

            """
            UPDATE alerts

            SET status='DONE'

            WHERE id=?

            """,

            (
                alert_id,
            )

        )



    conn.commit()

    conn.close()







# ==========================
# DISABLE ALERT AFTER HIT
# ==========================


def disable_alert(alert_id):


    remove_alert(alert_id)
