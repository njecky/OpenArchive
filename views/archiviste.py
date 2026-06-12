# ================================
# 📁 ARCHIVISTE DASHBOARD
# ================================

import tkinter as tk
from config.constants import *

class ArchivisteDashboard:

    def __init__(self, root, nom):

        self.root = root

        self.root.geometry("1200x700")
        self.root.configure(bg=WHITE)

        title = tk.Label(
            root,
            text=f"📁 Bienvenue Archiviste : {nom}",
            font=("Helvetica", 22, "bold"),
            bg=WHITE,
            fg=PRIMARY_COLOR
        )

        title.pack(pady=50)