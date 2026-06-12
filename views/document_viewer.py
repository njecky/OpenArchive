# ================================
# 📄 DOCUMENT VIEWER MODERNE
# ================================

import tkinter as tk
from tkinter import messagebox, simpledialog
import os

from config.constants import *
from config.function import open_file

import fitz  # PyMuPDF
from PIL import Image, ImageTk


# ================================
# 📄 VIEWER
# ================================
class DocumentViewer:

    def __init__(self, root, document_name, document_path):

        self.root = root
        self.document_name = document_name
        self.document_path = document_path

        self.zoom_level = 1.0
        self.dark_mode = False

        self.build_ui()
        self.load_document()

    # ================================
    # 🎨 UI
    # ================================
    def build_ui(self):

        self.window = tk.Toplevel(self.root)
        self.window.title(f"📄 {self.document_name}")
        self.window.geometry("1000x700")
        self.window.configure(bg=WHITE)

        # ================================
        # HEADER
        # ================================
        header = tk.Frame(self.window, bg=PRIMARY_COLOR, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=self.document_name,
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 12, "bold")
        ).pack(side="left", padx=15)

        # Boutons header
        tk.Button(
            header,
            text="🔍 Rechercher",
            command=self.search_text,
            bg=SECONDARY_COLOR,
            fg=WHITE,
            bd=0
        ).pack(side="right", padx=5)

        tk.Button(
            header,
            text="➕ Zoom",
            command=self.zoom_in,
            bg=SUCCESS_COLOR,
            fg=WHITE,
            bd=0
        ).pack(side="right", padx=5)

        tk.Button(
            header,
            text="➖ Zoom",
            command=self.zoom_out,
            bg=WARNING_COLOR,
            fg=WHITE,
            bd=0
        ).pack(side="right", padx=5)

        tk.Button(
            header,
            text="🌓 Mode",
            command=self.toggle_theme,
            bg=DARK_COLOR,
            fg=WHITE,
            bd=0
        ).pack(side="right", padx=5)

        tk.Button(
            header,
            text="📂 Ouvrir externe",
            command=self.open_external,
            bg=DANGER_COLOR,
            fg=WHITE,
            bd=0
        ).pack(side="right", padx=5)

        # ================================
        # BODY
        # ================================
        self.body = tk.Frame(self.window, bg=WHITE)
        self.body.pack(fill="both", expand=True)

        # Canvas image/pdf
        self.canvas = tk.Canvas(self.body, bg=WHITE)
        self.canvas.pack(fill="both", expand=True)

        # Text preview
        self.text_area = tk.Text(
            self.body,
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            font=("Consolas", 10),
            wrap="word"
        )

        # Ctrl+F
        self.window.bind("<Control-f>", lambda e: self.search_text())

    # ================================
    # 📄 LOAD
    # ================================
    def load_document(self):

        if not os.path.exists(self.document_path):
            messagebox.showerror("Erreur", "Fichier introuvable")
            return

        ext = os.path.splitext(self.document_path)[1].lower()

        # ================= PDF =================
        if ext == ".pdf":
            self.show_pdf()

        # ================= IMAGE =================
        elif ext in [".png", ".jpg", ".jpeg"]:
            self.show_image()

        # ================= TEXTE =================
        elif ext in [".txt", ".csv", ".log", ".md"]:
            self.show_text()

        else:
            self.show_text()
            self.text_area.insert("end", "\n\n⚠️ Aperçu non disponible. Utilisez ouvrir.")

    # ================================
    # 📄 TEXT VIEW
    # ================================
    def show_text(self):

        self.canvas.pack_forget()
        self.text_area.pack(fill="both", expand=True)

        with open(self.document_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        self.text_area.insert("1.0", content)
        self.text_area.config(state="disabled")

    # ================================
    # 🖼 IMAGE VIEW
    # ================================
    def show_image(self):

        self.text_area.pack_forget()
        self.canvas.pack(fill="both", expand=True)

        img = Image.open(self.document_path)
        img = img.resize(
            (
                int(img.width * self.zoom_level),
                int(img.height * self.zoom_level)
            )
        )

        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)

    # ================================
    # 📄 PDF VIEW
    # ================================
    def show_pdf(self):

        self.text_area.pack_forget()
        self.canvas.pack(fill="both", expand=True)

        doc = fitz.open(self.document_path)
        page = doc.load_page(0)

        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img = img.resize(
            (
                int(img.width * self.zoom_level),
                int(img.height * self.zoom_level)
            )
        )

        self.pdf_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.pdf_img)

    # ================================
    # 🔍 SEARCH
    # ================================
    def search_text(self):

        if not self.text_area.winfo_ismapped():
            messagebox.showinfo("Recherche", "Recherche disponible seulement en texte.")
            return

        query = simpledialog.askstring("Recherche", "Mot à rechercher :")

        if not query:
            return

        content = self.text_area.get("1.0", "end")

        index = content.lower().find(query.lower())

        if index == -1:
            messagebox.showinfo("Recherche", "Aucun résultat trouvé")
        else:
            messagebox.showinfo("Recherche", f"Trouvé à la position {index}")

    # ================================
    # 🔍 ZOOM IN
    # ================================
    def zoom_in(self):

        self.zoom_level += 0.1
        self.load_document()

    # ================================
    # 🔍 ZOOM OUT
    # ================================
    def zoom_out(self):

        if self.zoom_level > 0.3:
            self.zoom_level -= 0.1
            self.load_document()

    # ================================
    # 🌗 THEME
    # ================================
    def toggle_theme(self):

        self.dark_mode = not self.dark_mode

        bg = DARK_COLOR if self.dark_mode else WHITE
        fg = WHITE if self.dark_mode else TEXT_COLOR

        self.window.configure(bg=bg)
        self.body.configure(bg=bg)
        self.canvas.configure(bg=bg)
        self.text_area.configure(bg=bg, fg=fg)

    # ================================
    # 📂 OPEN EXTERNAL
    # ================================
    def open_external(self):

        try:
            open_file(self.document_path)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))