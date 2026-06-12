# # config/database.py
# import sqlite3
# import os

# DB_NAME = "desk.db"

# def get_connection():
#     """Ouvre une connexion SQLite et crée la base si nécessaire."""
#     conn = sqlite3.connect(DB_NAME)
#     return conn

# def init_db():
#     """Crée les tables si elles n'existent pas déjà."""
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS contacts (
#         id int PRIMARY KEY AUTOINCREMENT,
#         nom varchar(255) NOT NULL,
#         tel varchar(15) NOT NULL UNIQUE,
#         email varchar(30) UNIQUE,
#         category VARCHAR(12) DEFAULT 'Client'
#     )
#     """)

#     conn.commit()
#     conn.close()

# ================================
# 🗄️ Connexion à la DB - ArchivaDesk
# ================================

# import sqlite3
# # from config.constants import *
# import os

# # ================================
# # 🔌 Ouvrir la connexion
# # ================================
# def get_connection():
#     """Ouvre une connexion SQLite et crée la base si nécessaire."""
#     # Crée le dossier si besoin
#     db_dir = os.path.dirname(DB_PATH)
#     if db_dir and not os.path.exists(db_dir):
#         os.makedirs(db_dir)

#     conn = sqlite3.connect(DB_PATH)
#     return conn


# # ================================
# # 🏗️ Créer les tables
# # ================================
# def init_db():
#     """Crée toutes les tables nécessaires si elles n'existent pas."""
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Table roles
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS roles (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nom TEXT UNIQUE NOT NULL
#     )
#     """)

#     # Table users
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nom TEXT NOT NULL,
#         login TEXT UNIQUE NOT NULL,
#         password TEXT NOT NULL,
#         roly INTEGER,
#         FOREIGN KEY(roly) REFERENCES roles(id)
#     )
#     """)

#     # Table documents
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS documents (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nom TEXT,
#         chemin TEXT,
#         type TEXT,
#         date_ajout TEXT,
#         usy INTEGER,
#         FOREIGN KEY(usy) REFERENCES users(id)
#     )
#     """)

#     # Table logs
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS logs (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         action TEXT,
#         user_id INTEGER,
#         date TEXT,
#         FOREIGN KEY(user_id) REFERENCES users(id)
#     )
#     """)

#     conn.commit()
#     conn.close()

#     # Insérer les rôles par défaut
#     # insert_roles()

#     # Créer admin par défaut
#     # create_default_admin()


# # ================================
# # 👥 Insérer les rôles
# # ================================
# # def insert_roles():
# #     conn = get_connection()
# #     cursor = conn.cursor()

# #     roles = [ROLE_ADMIN, ROLE_ARCHIVISTE, ROLE_USER]

# #     for role in roles:
# #         cursor.execute("INSERT OR IGNORE INTO roles (nom) VALUES (?)", (role,))

# #     conn.commit()
# #     conn.close()


# # # ================================
# # # 🔑 Créer admin par défaut
# # # ================================
# # def create_default_admin():
# #     conn = get_connection()
# #     cursor = conn.cursor()

# #     # Récupérer l'id du rôle admin
# #     cursor.execute("SELECT id FROM roles WHERE nom = ?", (ROLE_ADMIN,))
# #     role = cursor.fetchone()

# #     if role:
# #         role_id = role[0]
# #         # Insérer l'admin si inexistant
# #         cursor.execute("""
# #         INSERT OR IGNORE INTO users (nom, login, mot_de_passe, role_id)
# #         VALUES (?, ?, ?, ?)
# #         """, ("Admin", "admin", "admin123", role_id))

# #     conn.commit()
# #     conn.close()


# # ================================
# # 🚀 Tester la connexion
# # ================================
# if __name__ == "__main__":
#     init_db()
#     print("✅ Base ArchivaDesk initialisée avec succès !")

# ================================
# 🔌 Connexion SQLite - ArchivaDesk
# ================================
# config/database.py
import sqlite3
import hashlib
from config.constants import *

DB_NAME = "desk.bd"  # Nom de la base

# ================================
# 🔹 Connexion à la base
# ================================
def get_connection():
    """Retourne un objet connexion SQLite"""
    return sqlite3.connect(DB_NAME)


# ================================
# 🔹 Fonction hash mot de passe
# ================================
def hash_password(password):
    """Hash le mot de passe avec SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


# ================================
# 🔹 Vérification login
# ================================
def check_login(login, password):
    """Vérifie si le login/mot de passe correspond à un utilisateur"""
    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    query = """
    SELECT u.id, u.nom, r.nom
    FROM users u
    LEFT JOIN roles r ON u.role_id = r.id
    WHERE u.login = ? AND u.mot_de_passe = ?
    """
    cursor.execute(query, (login, hashed))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Retour : id_utilisateur, nom, rôle
        return {"id": user[0], "nom": user[1], "role": user[2]}
    else:
        return None


# ================================
# 🔹 Création utilisateur
# ================================
def create_user(nom, login, password, role):
    """Crée un nouvel utilisateur"""
    conn = get_connection()
    cursor = conn.cursor()

    # Récupérer id rôle
    cursor.execute("SELECT id FROM roles WHERE nom = ?", (role,))
    role_id = cursor.fetchone()
    if not role_id:
        conn.close()
        return False

    role_id = role_id[0]
    hashed = hash_password(password)

    try:
        cursor.execute("""
        INSERT INTO users (nom, login, mot_de_passe, role_id)
        VALUES (?, ?, ?, ?)
        """, (nom, login, hashed, role_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Login déjà existant
        conn.close()
        return False


# ================================
# 🔹 Récupérer tous les utilisateurs
# ================================
def get_users():
    """Retourne tous les utilisateurs avec leur rôle"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id, u.nom, u.login, r.nom
    FROM users u
    LEFT JOIN roles r ON u.role_id = r.id
    """)
    users = cursor.fetchall()
    conn.close()
    return users