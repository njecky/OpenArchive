# ================================
# 🔐 AUTH CONTROLLER
# ================================

import sqlite3
from config.constants import *

# ================================
# 🔹 LOGIN USER
# ================================
def login_user(login, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.id,
               users.nom,
               users.login,
               roles.name
        FROM users
        JOIN roles
        ON users.role_id = roles.id
        WHERE users.login = ?
        AND users.mot_de_passe = ?
    """, (login, password))

    user = cursor.fetchone()

    conn.close()

    return user