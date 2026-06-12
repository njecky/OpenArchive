# ================================
# ⚙️ FUNCTIONS - ArchivaDesk
# ================================

import os
import platform
import subprocess
from tkinter import filedialog
from tkinter import messagebox

# ================================
# 📂 OUVRIR FICHIER SYSTÈME
# ================================
def open_file(filepath):

    try:

        system_name = platform.system()

        # WINDOWS
        if system_name == "Windows":

            os.startfile(filepath)

        # MAC
        elif system_name == "Darwin":

            subprocess.call(["open", filepath])

        # LINUX
        else:

            subprocess.call(["xdg-open", filepath])

    except Exception as error:

        messagebox.showerror(
            "Erreur",
            f"Impossible d'ouvrir le fichier.\n\n{error}"
        )


# ================================
# 📁 CHOISIR FICHIER
# ================================
def choose_document():

    filetypes = [

        ("Documents PDF", "*.pdf"),
        ("Documents Word", "*.docx"),
        ("Documents Excel", "*.xlsx"),
        ("Images", "*.png *.jpg *.jpeg"),
        ("Tous les fichiers", "*.*")

    ]

    file_path = filedialog.askopenfilename(
        title="Sélectionner un document",
        filetypes=filetypes
    )

    return file_path


# ================================
# 📦 TAILLE FICHIER
# ================================
def get_file_size(filepath):

    try:

        size = os.path.getsize(filepath)

        # KB
        if size < 1024 * 1024:

            return f"{round(size / 1024, 2)} KB"

        # MB
        else:

            return f"{round(size / (1024 * 1024), 2)} MB"

    except:

        return "0 KB"


# ================================
# 📄 EXTENSION
# ================================
def get_file_extension(filepath):

    extension = os.path.splitext(filepath)[1]

    return extension.replace(".", "").upper()


# ================================
# 🖼️ ICON DOCUMENT
# ================================
def get_document_icon(extension):

    extension = extension.lower()

    icons = {

        "pdf": "📄",
        "docx": "📝",
        "xlsx": "📊",
        "png": "🖼",
        "jpg": "🖼",
        "jpeg": "🖼"

    }

    return icons.get(extension, "📁")

# ================================
# ⬇ TÉLÉCHARGER DOCUMENT
# ================================
def download_selected_document(self):

    selected = self.document_table.selection()

    if not selected:

        messagebox.showwarning(
            "Téléchargement",
            "Veuillez sélectionner un document."
        )

        return

    values = self.document_table.item(
        selected[0],
        "values"
    )

    document_name = values[0]

    # Simulation téléchargement (tu pourras connecter DB / fichier réel après)
    messagebox.showinfo(
        "Téléchargement",
        f"Téléchargement du document :\n\n{document_name}"
    )