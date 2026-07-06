# ================================
# 🔐 Login Window - ArchivaDesk (UI/UX Moderne)
# ================================

import tkinter as tk
from config.constants import *
from tkinter import font as tkfont
from controllers.auth_controller import login_user

class LoginWindow:
    def __init__(self, root):
        self.root = root
        
        # ================================
        # 🔐 ÉTAT DE LA CONNEXION
        # ================================
        # Empêche plusieurs tentatives de connexion simultanées
        self.is_logging_in = False

        # Couleur de fond principale
        self.root.configure(bg=PRIMARY_COLOR)

        # Taille et position centrée
        width = LOGIN_WIDTH + 100  # Card plus large que précédent
        height = LOGIN_HEIGHT + 100
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)

        # ================================
        # 🖼️ Conteneur principal (card)
        # ================================
        card = tk.Frame(
            self.root,
            bg=WHITE,
            width=LOGIN_WIDTH,
            height=LOGIN_HEIGHT,
            bd=0,
            relief="ridge"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        try:
            self.logo = tk.PhotoImage(file=IMAGES_PATH + "logo.png")
            logo_label = tk.Label(card, image=self.logo, bg=WHITE)
            logo_label.pack(pady=(10, 5))
        except:
            logo_label = tk.Label(
                card, text="📁", font=("Helvetica", 30), bg=WHITE, fg=PRIMARY_COLOR
            )
            logo_label.pack(pady=(10, 5))

        # Titre
        title = tk.Label(
            card,
            text="Connexion",
            font=("Helvetica", 20, "bold"),
            bg=WHITE,
            fg=PRIMARY_COLOR
        )
        title.pack(pady=(0, 15))

        # ================================
        # Champs Login et Mot de passe
        # ================================
        self.login_entry = self.create_entry(card, "Login")
        self.password_entry = self.create_entry(card, "Mot de passe", show="*")

        # ================================
        # Bouton Connexion
        # ================================
        self.login_btn = tk.Button(
            card,
            text="Se connecter",
            bg=SECONDARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 12, "bold"),
            width=20,
            relief="flat",
            command=self.login,
            activebackground=PRIMARY_COLOR,
            cursor="hand2"
        )
        self.login_btn.pack(pady=15)
        # Touche Entrée clavier
        # self.root.bind("<Return>", lambda event: self.login())
        # ================================
        # ⌨️ TOUCHE ENTRÉE
        # ================================
        self.root.bind("<Return>", self.on_enter_pressed)

        # Message
        self.message = tk.Label(card, text="", fg=DANGER_COLOR, bg=WHITE, font=("Helvetica", 10))
        self.message.pack()

    # ================================
    # Fonction helper pour créer Entry stylé
    # ================================
    def create_entry(self, parent, placeholder, show=None):
        frame = tk.Frame(parent, bg=LIGHT_COLOR, bd=0)
        frame.pack(pady=5, padx=20, fill="x")

        entry = tk.Entry(
            frame,
            bd=0,
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            font=("Helvetica", 12),
            show=show
        )
        entry.pack(ipady=8, fill="x", padx=10)

        # Placeholder simulé
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e, ph=placeholder: self.on_focus_in(entry, ph))
        entry.bind("<FocusOut>", lambda e, ph=placeholder: self.on_focus_out(entry, ph))

        return entry

    def on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg=TEXT_COLOR)

    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")
            
            
    # ================================
    # ⌨️ GESTION DE LA TOUCHE ENTRÉE
    # ================================
    def on_enter_pressed(self, event=None):

        if not self.is_logging_in:
            self.login()

    # ================================
    # 🔐 LOGIQUE DE CONNEXION
    # ================================
    def login(self):

        # Évite les doubles clics
        if self.is_logging_in:
            return

        self.is_logging_in = True

        self.login_btn.config(state="disabled")

        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        # ================================
        # VÉRIFICATION DES CHAMPS
        # ================================
        if login in ("", "Login") or password in ("", "Mot de passe"):

            self.message.config(
                text="Veuillez remplir tous les champs.",
                fg=DANGER_COLOR
            )

            self.login_btn.config(state="normal")
            self.is_logging_in = False

            return

        # ================================
        # AUTHENTIFICATION
        # ================================
        user = login_user(login, password)

        if not user:

            self.message.config(
                text="Login ou mot de passe incorrect.",
                fg=DANGER_COLOR
            )

            self.login_btn.config(state="normal")
            self.is_logging_in = False
            return

        # ================================
        # CONNEXION RÉUSSIE
        # ================================
        user_id, nom, username, role = user[:4]

        print("ID :", user_id)
        print("Nom :", nom)
        print("Login :", username)
        print("Rôle :", role)

        self.message.config(
            text="Connexion réussie",
            fg=SUCCESS_COLOR
        )

        # Désactive la touche Entrée
        self.root.unbind("<Return>")

        # Redirection
        self.root.after(
            500,
            lambda: self.redirect_user(role, nom)
        )
        
    # ================================
    # 🚀 REDIRECTION SELON LE RÔLE
    # ================================
    def redirect_user(self, role, nom):

        # Nettoyage de la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()

        # ================================
        # ADMIN
        # ================================
        if role == "Admin":

            from views.admin import AdminDashboard
            AdminDashboard(self.root, nom)

        # ================================
        # ARCHIVISTE
        # ================================
        elif role == "Archiviste":

            from views.archiviste import ArchivisteDashboard
            ArchivisteDashboard(self.root, nom)

        # ================================
        # UTILISATEUR
        # ================================
        elif role == "Utilisateur":

            from views.u import UserDashboard
            UserDashboard(self.root, nom)