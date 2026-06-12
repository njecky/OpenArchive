# ================================
# 👥 USER CONTROLLER
# ================================

import sqlite3
from config.constants import *

# ================================
# 🔍 CHECK LOGIN EXISTS
# ================================
def login_exists(login):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE login = ?",
        (login,)
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None


# ================================
# ➕ ADD USER
# ================================
def create_user(nom, login, mot_de_passe, role_name):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:

        # ================================
        # 🔍 GET ROLE ID
        # ================================
        cursor.execute(
            "SELECT id FROM roles WHERE name = ?",
            (role_name,)
        )

        role = cursor.fetchone()

        if not role:
            return False, "Rôle introuvable"

        role_id = role[0]

        # ================================
        # ➕ INSERT USER
        # ================================
        cursor.execute("""
            INSERT INTO users (
                nom,
                login,
                mot_de_passe,
                role_id
            )
            VALUES (?, ?, ?, ?)
        """, (
            nom,
            login,
            mot_de_passe,
            role_id
        ))

        conn.commit()

        return True, "Utilisateur ajouté"

    except sqlite3.Error as e:

        return False, str(e)

    finally:
        conn.close()