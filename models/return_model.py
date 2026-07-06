# ================================
# 📦 RETURN MODEL - DigiBox
# ================================

import sqlite3
from config.constants import DB_PATH


# ================================
# 📥 AJOUT RETOUR
# ================================
def add_return_document(document_id, document_name, borrower_name, borrower_phone, return_date, user_id, ip_address):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS return_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            document_name TEXT,
            borrower_name TEXT,
            borrower_phone TEXT,
            return_date TEXT,
            user_id INTEGER,
            ip_address TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO return_documents (
            document_id,
            document_name,
            borrower_name,
            borrower_phone,
            return_date,
            user_id,
            ip_address
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        document_id,
        document_name,
        borrower_name,
        borrower_phone,
        return_date,
        user_id,
        ip_address
    ))

    conn.commit()
    conn.close()


# ================================
# 📄 LISTE
# ================================
def get_all_returns():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM return_documents ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


# ================================
# 🔍 RETOUR PAR DOCUMENT
# ================================
def get_return_by_document(document_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM return_documents WHERE document_id=?
    """, (document_id,))

    row = cursor.fetchone()
    conn.close()

    return row


# ================================
# 🔄 MARK DOCUMENT RETURNED (optionnel)
# ================================
def mark_document_as_returned(document_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE documents
        SET status = 'Returned'
        WHERE id = ?
    """, (document_id,))

    conn.commit()
    conn.close()