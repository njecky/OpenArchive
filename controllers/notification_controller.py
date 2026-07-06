import sqlite3
from config.constants import DB_PATH
from datetime import datetime, date


# ================================
# 🔔 DOCUMENTS EN RETARD
# ================================
def get_overdue_documents():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, document_name, borrower_name,
               expected_return, expected_return_time
        FROM physical_document_loans
        WHERE returned = 0
        AND date(expected_return) < date('now','localtime')
        ORDER BY expected_return ASC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


# ================================
# ⏰ DOCUMENTS AUJOURD'HUI
# ================================
def get_today_documents():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, document_name, borrower_name,
               expected_return, expected_return_time
        FROM physical_document_loans
        WHERE returned = 0
        AND date(expected_return) = date('now','localtime')
    """)

    data = cursor.fetchall()
    conn.close()
    return data


# ================================
# ⚠️ PROCHES EXPIRATION (3 jours)
# ================================
def get_upcoming_documents():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, document_name, borrower_name,
               expected_return, expected_return_time
        FROM physical_document_loans
        WHERE returned = 0
        AND date(expected_return) BETWEEN date('now','localtime')
                                    AND date('now','localtime','+3 day')
        ORDER BY expected_return ASC
    """)

    data = cursor.fetchall()
    conn.close()
    return data