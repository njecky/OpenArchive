# ================================
# 📦 APPLICATION : DigiBox
# ================================
import os
import sys

APP_NAME = "OpenArchive"
APP_VERSION = "1.0.0"

# ================================
# 📁 DOSSIER APPLICATION
# ================================
if getattr(sys, "frozen", False):
    # Exécutable PyInstaller
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Mode développement
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(BASE_DIR)

# ================================
# 🗄️ DOSSIER DONNÉES UTILISATEUR
# ================================
APP_DATA_DIR = os.path.join(
    os.getenv("APPDATA"),
    APP_NAME
)

os.makedirs(APP_DATA_DIR, exist_ok=True)

# ================================
# 🗄️ BASE DE DONNÉES
# ================================
DB_PATH = os.path.join(
    APP_DATA_DIR,
    "database.db"
)

# ================================
# 📁 RESSOURCES
# ================================
ASSETS_PATH = os.path.join(
    BASE_DIR,
    "assets"
)

IMAGES_PATH = os.path.join(
    ASSETS_PATH,
    "images"
)

FONTS_PATH = os.path.join(
    ASSETS_PATH,
    "fonts"
)

# ================================
# 📁 DOCUMENTS ARCHIVÉS
# ================================
ARCHIVE_PATH = os.path.join(
    APP_DATA_DIR,
    "archives"
)

os.makedirs(
    ARCHIVE_PATH,
    exist_ok=True
)

# ================================
# 🎨 COULEURS (UI)
# ================================
PRIMARY_COLOR = "#2C3E50"     # Bleu sombre
SECONDARY_COLOR = "#3498DB"   # Bleu clair
SUCCESS_COLOR = "#2ECC71"     # Vert
DANGER_COLOR = "#E74C3C"      # Rouge
WARNING_COLOR = "#F39C12"     # Orange
LIGHT_COLOR = "#ECF0F1"       # Gris clair
DARK_COLOR = "#1A252F"        # Noir doux

TEXT_COLOR = "#2C3E50"
WHITE = "#FFFFFF"

# ================================
# 🖥️ DIMENSIONS FENÊTRES
# ================================
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

LOGIN_WIDTH = 400
LOGIN_HEIGHT = 300

# ================================
# 🔐 RÔLES
# ================================
ROLE_ADMIN = "Admin"
ROLE_ARCHIVISTE = "Archiviste"
ROLE_USER = "Utilisateur"

ROLES = [
    ROLE_ADMIN,
    ROLE_ARCHIVISTE,
    ROLE_USER
]

# ================================
# 🔑 ACTIONS
# ================================
ACTION_ADD = "add"
ACTION_EDIT = "edit"
ACTION_DELETE = "delete"
ACTION_VIEW = "view"

# ================================
# 🧠 MESSAGES
# ================================
LOGIN_SUCCESS = "Connexion réussie"
LOGIN_ERROR = "Identifiants incorrects"

ACCESS_DENIED = "Accès refusé"
ACTION_SUCCESS = "Action réalisée avec succès"
ACTION_ERROR = "Une erreur est survenue"

# ================================
# 📄 TYPES DE FICHIERS
# ================================
ALLOWED_FILE_TYPES = [
    ".pdf",
    ".docx",
    ".xlsx",
    ".png",
    ".jpg",
    ".jpeg"
]

# ================================
# 📅 FORMAT DATE
# ================================
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"