# ================================
# 🗄️ MODEL - ArchivaDesk
# ================================

import sqlite3
import socket
import requests   # 👈 AJOUT ICI
import platform
from config.constants import *
# import socket
# import requests

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=3).text
    except:
        return "unknown"

# ================================
# 🔹 CONNEXION DB
# ================================
def connect_db():
    return sqlite3.connect(DB_PATH)

# ================================
# 🔹 INITIALISATION DB
# ================================
def init_db():

    conn = connect_db()
    cursor = conn.cursor()

    # ================================
    # 📁 TABLE ROLES
    # ================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # ================================
    # 👤 TABLE USERS
    # ================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY(role_id) REFERENCES roles(id)
        )
    """)

    # ================================
    # 📁 TABLE DOCUMENTS
    # ================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT NOT NULL UNIQUE,

            type TEXT NOT NULL,

            categorie TEXT,

            tags TEXT,

            taille TEXT,

            chemin TEXT NOT NULL,

            user_id INTEGER NOT NULL,

            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,

            statut TEXT DEFAULT 'Actif',

            FOREIGN KEY(user_id) REFERENCES users(id)

        )
    """)
    
    # ================================
    # 📊 TABLE DOCUMENT ACTIVITIES
    # ================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_activities (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            document_id INTEGER,

            user_id INTEGER,

            document_name TEXT NOT NULL,

            action TEXT NOT NULL,

            ip_address TEXT,

            date_action DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(document_id)
                REFERENCES documents(id),

            FOREIGN KEY(user_id)
                REFERENCES users(id)

        )
    """)
    
    # ================================
    # 📁 TABLE DOCUMENTS PHYSIQUES
    # ================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS physical_document_loans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            borrower_name TEXT NOT NULL,

            borrower_service TEXT,

            borrower_phone TEXT,

            document_name TEXT NOT NULL,

            document_reference TEXT,

            reason TEXT,

            loan_date DATE DEFAULT (DATE('now','localtime')),

            loan_time TIME DEFAULT (TIME('now','localtime')),

            expected_return DATE NOT NULL,

            expected_return_time TIME NOT NULL,

            returned INTEGER DEFAULT 0,

            return_date DATE,

            return_time TIME,

            status TEXT DEFAULT 'Sorti',

            notes TEXT

        )
    """)
    
    # =====================================================
    # 🧪 MODE DÉVELOPPEMENT UNIQUEMENT
    # -----------------------------------------------------
    # Ce bloc supprime automatiquement tous les emprunts
    # de documents physiques à chaque démarrage de
    # l'application et réinitialise l'AUTOINCREMENT.
    #
    # ⚠️ IMPORTANT :
    # À SUPPRIMER ou À COMMENTER avant la mise en production,
    # sinon toutes les données seront effacées à chaque lancement.
    # =====================================================


    # Supprime tous les enregistrements
    # cursor.execute("""
    #     DELETE FROM physical_document_loans
    # """)

    # # Réinitialise l'identifiant AUTO_INCREMENT (le prochain ID sera 1)
    # cursor.execute("""
    #     DELETE FROM sqlite_sequence
    #     WHERE name = 'physical_document_loans'
    # """)
    # ================================
    # 🔐 INSERT ROLES
    # ================================
    roles = [
        ("Admin",),
        ("Archiviste",),
        ("Utilisateur",)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO roles(name)
        VALUES(?)
    """, roles)

    # ================================
    # 👑 USERS DEFAULT
    # ================================
    create_user(cursor, "Admin", "admin", "admin123", "Admin")
    create_user(cursor, "Archiviste", "archiviste", "arch123", "Archiviste")
    create_user(cursor, "Utilisateur Standard", "user", "user123", "Utilisateur")

    conn.commit()

    print("✅ Base de données initialisée")

    conn.close()

# ================================
# 🔹 CREATE USER
# ================================
def create_user(cursor, nom, login, password, role_name):

    cursor.execute("""
        SELECT id FROM users WHERE login = ?
    """, (login,))

    if cursor.fetchone():
        return

    cursor.execute("""
        SELECT id FROM roles WHERE name = ?
    """, (role_name,))

    role = cursor.fetchone()

    if role:

        cursor.execute("""
            INSERT INTO users(nom, login, mot_de_passe, role_id)
            VALUES (?, ?, ?, ?)
        """, (
            nom,
            login,
            password,
            role[0]
        ))

        print(f"✅ Utilisateur créé : {login}")

# ================================
# 🔍 GET USERS
# ================================
def get_users():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.id, users.nom, users.login, roles.name
        FROM users
        JOIN roles ON users.role_id = roles.id
        ORDER BY users.id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data

# ================================
# ➕ ADD USER
# ================================
def add_user_db(nom, login, password, role_name):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
    if cursor.fetchone():
        return {"success": False, "message": "Login déjà utilisé"}

    cursor.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
    role = cursor.fetchone()

    if not role:
        return {"success": False, "message": "Rôle introuvable"}

    cursor.execute("""
        INSERT INTO users(nom, login, mot_de_passe, role_id)
        VALUES (?, ?, ?, ?)
    """, (nom, login, password, role[0]))

    conn.commit()
    conn.close()

    return {"success": True, "message": "Utilisateur ajouté"}

# ================================
# 📄 ADD DOCUMENT
# ================================
def add_document(nom, type_doc, categorie, tags, taille, chemin, user_id):

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO documents (
                nom,
                type,
                categorie,
                tags,
                taille,
                chemin,
                user_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            nom,
            type_doc,
            categorie,
            tags,
            taille,
            chemin,
            user_id
        ))

        conn.commit()

        return {"success": True, "message": "Document ajouté"}

    except sqlite3.IntegrityError:
        return {"success": False, "message": "Nom de document déjà utilisé"}

    finally:
        conn.close()

# ================================
# 📄 GET DOCUMENTS
# ================================
def get_documents():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nom,
            type,
            categorie,
            tags,
            taille,
            date_creation,
            chemin
        FROM documents
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data

# ================================
# 📊 TOTAL DOCUMENTS PAR TYPE
# ================================
def count_documents_by_type(type_doc):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM documents
        WHERE type = ?
    """, (type_doc,))

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ================================
# 📊 TOTAL DOCUMENTS
# ================================
def count_all_documents():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM documents
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

# ================================
# 📄 GET DOCUMENT BY ID
# ================================
def get_document_by_id(document_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nom,
            type,
            categorie,
            tags,
            taille,
            chemin,
            date_creation
        FROM documents
        WHERE id = ?
    """, (document_id,))

    document = cursor.fetchone()

    conn.close()

    return document

# ================================
# 🗑 DELETE DOCUMENT BY ID
# ================================
def delete_document_by_id(document_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT chemin FROM documents WHERE id = ?
    """, (document_id,))

    result = cursor.fetchone()

    if not result:
        conn.close()
        return None

    file_path = result[0]

    cursor.execute("""
        DELETE FROM documents WHERE id = ?
    """, (document_id,))

    conn.commit()
    conn.close()

    return file_path

# ================================
# 📊 TOTAL TÉLÉCHARGEMENTS
# ================================
def count_downloads():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM document_activities
        WHERE action = 'Téléchargement'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ================================
# 📊 TOTAL MODIFICATIONS
# ================================
def count_edits():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM document_activities
        WHERE action = 'Modification'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

# ================================
# 📊 TOTAL SUPPRESSIONS
# ================================
def count_deletes():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM document_activities
        WHERE action = 'Suppression'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

# ================================
# 📊 UTILISATEURS ACTIFS
# ================================
def count_active_users():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM document_activities
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

# ================================
# 📝 AJOUT ACTIVITÉ DOCUMENT
# ================================
def add_document_activity(
    document_id,
    document_name,
    user_id,
    action,
    ip_address
):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO document_activities(

            document_id,
            document_name,
            user_id,
            action,
            ip_address

        )

         VALUES (?, ?, ?, ?, ?)

    """, (

        document_id,
        document_name,
        user_id,
        action,
        ip_address

    ))

    conn.commit()
    conn.close()
    
    
# ================================
# 📝 AJOUT ACTIVITÉ DOCUMENT
# ================================
def add_document_activity(
    document_id,
    document_name,
    user_id,
    action,
    ip_address
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO document_activities(

            document_id,
            document_name,
            user_id,
            action,
            ip_address

        )

        VALUES (?, ?, ?, ?, ?)

    """, (

        document_id,
        document_name,
        user_id,
        action,
        ip_address

    ))

    conn.commit()

    conn.close()
    

# ================================
# 👁 TOTAL CONSULTATIONS (OUVERTURES)
# ================================
def count_views():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM document_activities
        WHERE action = 'Consultation'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

# ================================
# 📋 GET DOCUMENT ACTIVITIES
# ================================
def get_document_activities():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            da.document_name,
            u.nom,
            da.action,
            DATE(da.date_action),
            TIME(da.date_action),
            da.ip_address

        FROM document_activities da

        LEFT JOIN users u
            ON da.user_id = u.id

        ORDER BY da.date_action DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ================================
# 📋 GET DOCUMENT ACTIVITIES
# ================================
def get_document_activities(keyword="", action="Toutes"):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
        SELECT
            da.document_name,
            u.nom,
            da.action,
            DATE(da.date_action),
            TIME(da.date_action),
            da.ip_address
        FROM document_activities da

        LEFT JOIN users u
            ON da.user_id = u.id

        WHERE 1=1
    """

    params = []

    # 🔎 Recherche
    if keyword.strip():
        query += """
            AND da.document_name LIKE ?
        """
        params.append(f"%{keyword}%")

    # 🎯 Filtre action
    if action != "Toutes":
        query += """
            AND da.action = ?
        """
        params.append(action)

    query += """
        ORDER BY da.date_action DESC
    """

    cursor.execute(query, params)

    results = cursor.fetchall()

    conn.close()

    return results


# ================================
# 🔎 LINEAR SEARCH ACTIVITIES
# ================================
def search_document_activities_linear(
    keyword="",
    action_filter="Toutes"
):

    activities = get_document_activities()

    results = []

    keyword = keyword.lower().strip()

    for activity in activities:

        document = str(activity[0]).lower()
        user = str(activity[1]).lower()
        action = str(activity[2]).lower()
        date = str(activity[3]).lower()
        heure = str(activity[4]).lower()
        ip = str(activity[5]).lower()

        # ================================
        # RECHERCHE MOT CLÉ
        # ================================
        found = (
            keyword in document or
            keyword in user or
            keyword in action or
            keyword in date or
            keyword in heure or
            keyword in ip
        )

        # ================================
        # FILTRE ACTION
        # ================================
        if action_filter != "Toutes":

            if found and action == action_filter.lower():
                results.append(activity)

        else:

            if found:
                results.append(activity)

    return results

# ================================
# 📊 TOTAL DOCUMENTS PHYSIQUES
# ================================
def count_physical_documents():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM physical_document_loans
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ================================
# 📊 DOCUMENTS SORTIS
# ================================
def count_physical_out():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM physical_document_loans
        WHERE returned = 0
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ================================
# 📊 DOCUMENTS RETOURNÉS
# ================================
def count_physical_returned():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM physical_document_loans
        WHERE returned = 1
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ================================
# 📊 DOCUMENTS EN RETARD
# ================================
def count_physical_late():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM physical_document_loans
        WHERE returned = 0
        AND DATE(expected_return) < DATE('now','localtime')
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

# ================================
# 📊 RETOURS PRÉVUS AUJOURD'HUI
# ================================
def count_due_today():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM physical_document_loans
        WHERE returned = 0
        AND expected_return = DATE('now','localtime')
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

# ================================
# 📊 EMPRUNTEURS UNIQUES
# ================================
def count_unique_borrowers():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT borrower_name)
        FROM physical_document_loans
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ================================
# 📌 CHARGER LES EMPRUNTS DE DOCUMENTS PHYSIQUES
# ================================
def get_physical_document_loans():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            document_name,
            document_reference,
            borrower_name,

            strftime('%d/%m/%Y', loan_date) AS loan_date,

            loan_time,

            strftime('%d/%m/%Y', expected_return) AS expected_return,

            expected_return_time,

            status

        FROM physical_document_loans

        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

# ================================
# 🔔 DOCUMENTS À RESTITUER AUJOURD'HUI
# ================================
def get_due_today_documents():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            id,
            borrower_name,
            borrower_service,
            borrower_phone,
            document_name,
            expected_return,
            expected_return_time

        FROM physical_document_loans

        WHERE returned = 0
        AND expected_return = DATE('now','localtime')

        ORDER BY expected_return_time

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ================================
# ✅ MARQUER UN DOCUMENT COMME RESTITUÉ
# ================================
def mark_document_returned(loan_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE physical_document_loans
        SET
            returned = 1,
            status = 'Retourné',
            actual_return = DATE('now','localtime')
        WHERE id=?
    """,(loan_id,))

    conn.commit()
    conn.close()

# ================================
# 🗑️ SUPPRIMER TOUS LES EMPRUNTS
# (Réinitialise également l'AUTOINCREMENT)
# ================================
# def clear_physical_document_loans():

#     conn = connect_db()
#     cursor = conn.cursor()

#     try:
#         # Supprime toutes les lignes
#         cursor.execute("""
#             DELETE FROM physical_document_loans
#         """)

#         # Réinitialise le compteur AUTOINCREMENT
#         cursor.execute("""
#             DELETE FROM sqlite_sequence
#             WHERE name = 'physical_document_loans'
#         """)

#         conn.commit()

#         return {
#             "success": True,
#             "message": "Tous les emprunts ont été supprimés."
#         }

#     except Exception as e:

#         conn.rollback()

#         return {
#             "success": False,
#             "message": str(e)
#         }

#     finally:
#         conn.close()