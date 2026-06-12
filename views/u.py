import tkinter as tk
from config.constants import *

class UserDashboard:

    def __init__(self, root, nom):

        self.root = root
        self.nom = nom

        self.root.configure(bg=LIGHT_COLOR)

        # ================================
        # HEADER
        # ================================
        header = tk.Frame(self.root, bg=PRIMARY_COLOR, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text=f"👤 Bienvenue {nom} - Espace Utilisateur",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 14, "bold")
        )
        title.pack(side="left", padx=15)

        # ================================
        # BODY
        # ================================
        body = tk.Frame(self.root, bg=LIGHT_COLOR)
        body.pack(fill="both", expand=True)

        # ================================
        # 📊 STATS SIMPLES
        # ================================
        stats = tk.Frame(body, bg=LIGHT_COLOR)
        stats.pack(pady=20)

        self.card(stats, "📁 Mes documents", "0", SECONDARY_COLOR)
        self.card(stats, "📥 Téléchargements", "0", SUCCESS_COLOR)
        self.card(stats, "⭐ Favoris", "0", WARNING_COLOR)

        # ================================
        # 📂 ACTIONS
        # ================================
        actions = tk.Frame(body, bg=LIGHT_COLOR)
        actions.pack(pady=30)

        tk.Button(
            actions,
            text="📁 Voir mes documents",
            bg=SECONDARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=10,
            bd=0,
            cursor="hand2"
        ).pack(pady=5)

        tk.Button(
            actions,
            text="📥 Télécharger un document",
            bg=SUCCESS_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=10,
            bd=0,
            cursor="hand2"
        ).pack(pady=5)

        tk.Button(
            actions,
            text="🔍 Rechercher",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=10,
            bd=0,
            cursor="hand2"
        ).pack(pady=5)

        # ================================
        # FOOTER
        # ================================
        footer = tk.Frame(self.root, bg=LIGHT_COLOR)
        footer.pack(side="bottom", fill="x")

        tk.Label(
            footer,
            text="ArchivaDesk - Espace Utilisateur",
            bg=LIGHT_COLOR,
            fg="gray"
        ).pack(pady=5)

    # ================================
    # 📦 CARD
    # ================================
    def card(self, parent, title, value, color):

        frame = tk.Frame(parent, bg=WHITE, width=180, height=90)
        frame.pack(side="left", padx=10)
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10)
        ).pack(pady=10)

        tk.Label(
            frame,
            text=value,
            bg=WHITE,
            fg=color,
            font=("Helvetica", 18, "bold")
        ).pack()