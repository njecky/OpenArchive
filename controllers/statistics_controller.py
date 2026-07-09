# ================================
# 📊 STATISTICS CONTROLLER
# ================================

import sqlite3
from config.constants import DB_PATH


# ================================
# 📄 TOTAL DOCUMENTS EMPRUNTÉS
# ================================
def get_total_loans():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM physical_document_loans
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result



# ================================
# ✅ DOCUMENTS RETOURNÉS
# ================================
def get_total_returned():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM physical_document_loans
        WHERE returned = 1
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result



# ================================
# 🚨 DOCUMENTS EN RETARD
# ================================
def get_total_overdue():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
        SELECT COUNT(*)

        FROM physical_document_loans

        WHERE returned = 0

        AND
        (
            date(expected_return)
            < date('now','localtime')

            OR

            (
            date(expected_return)
            = date('now','localtime')

            AND

            time(expected_return_time)
            < time('now','localtime')
            )

        )

    """)


    result = cursor.fetchone()[0]


    conn.close()


    return result



# ================================
# 📅 RETOURS PRÉVUS AUJOURD'HUI
# ================================
def get_today_returns():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
        SELECT COUNT(*)

        FROM physical_document_loans

        WHERE returned = 0

        AND date(expected_return)
        =
        date('now','localtime')

    """)


    result = cursor.fetchone()[0]


    conn.close()


    return result



# ================================
# ⏳ RETOURS À VENIR (J+1 à J+7)
# ================================
def get_upcoming_returns():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
        SELECT COUNT(*)

        FROM physical_document_loans

        WHERE returned = 0

        AND date(expected_return)

        BETWEEN

        date('now','localtime','+1 day')

        AND

        date('now','localtime','+7 day')

    """)


    result = cursor.fetchone()[0]


    conn.close()


    return result



# ================================
# 📈 TAUX DE RETOUR
# ================================
def get_return_rate():

    total = get_total_loans()

    returned = get_total_returned()


    if total == 0:

        return 0


    rate = (returned / total) * 100


    return round(rate, 2)



# ================================
# 📊 TOUTES LES STATISTIQUES
# ================================
def get_statistics():

    return {

        "total_loans":
            get_total_loans(),

        "returned":
            get_total_returned(),

        "overdue":
            get_total_overdue(),

        "today":
            get_today_returns(),

        "upcoming":
            get_upcoming_returns(),

        "rate":
            get_return_rate()
    }