# ================================
# 📦 RETURN CONTROLLER
# ================================
import sqlite3
from config.constants import DB_PATH
from datetime import datetime


# ================================
# 📄 DOCUMENTS À RETOURNER
# ================================
def get_pending_returns():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            document_name,
            borrower_name,
            borrower_phone,
            expected_return,
            expected_return_time,
            status
        FROM physical_document_loans
        WHERE returned = 0
        ORDER BY expected_return ASC, expected_return_time ASC
    """)

    data = cursor.fetchall()
    conn.close()

    return data


# ================================
# 📥 MARQUER COMME RETOURNÉ
# ================================
def mark_document_returned(document_id, user_id=1):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE physical_document_loans
        SET returned = 1,
            status = 'Returned',
            return_date = DATE('now','localtime'),
            return_time = TIME('now','localtime')
        WHERE id = ?
    """, (document_id,))

    conn.commit()
    conn.close()

    return True

# ================================
# 📝 LOG RETOUR
# ================================
def add_return_log(document_id, action="Retour document"):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO document_logs (document_id, action, created_at)
        VALUES (?, ?, datetime('now','localtime'))
    """, (document_id, action))

    conn.commit()
    conn.close()