# ================================
# 🖼️ Splash Screen - ArchivaDesk
# ================================

import tkinter as tk
from tkinter import ttk
from config.constants import *

class SplashScreen:
    def __init__(self, root):
        self.root = root

        # Création d'une fenêtre splash indépendante
        self.splash = tk.Toplevel()
        self.splash.title(APP_NAME)
        self.splash.overrideredirect(True)  # Supprimer barre de titre

        # Taille et position (centré écran)
        width = 500
        height = 300
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        self.splash.configure(bg=PRIMARY_COLOR)

        # ================================
        # 🖼️ CONTENU
        # ================================

        container = tk.Frame(self.splash, bg=PRIMARY_COLOR)
        container.pack(expand=True, fill="both")

        try:
            self.logo = tk.PhotoImage(file=IMAGES_PATH + "logo.png")
            logo_label = tk.Label(container, image=self.logo, bg=PRIMARY_COLOR)
            logo_label.pack(pady=10)
        except:
            logo_label = tk.Label(container, text="📁", font=("Arial", 40), bg=PRIMARY_COLOR, fg=WHITE)
            logo_label.pack(pady=10)

        app_label = tk.Label(container, text=APP_NAME, font=("Helvetica", 20, "bold"), bg=PRIMARY_COLOR, fg=WHITE)
        app_label.pack(pady=5)

        self.loading_label = tk.Label(container, text="Chargement...", font=("Arial", 10), bg=PRIMARY_COLOR, fg=LIGHT_COLOR)
        self.loading_label.pack(pady=5)

        self.progress = ttk.Progressbar(container, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=15)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", thickness=8, troughcolor=LIGHT_COLOR, background=SECONDARY_COLOR, bordercolor=PRIMARY_COLOR)

        self.progress['value'] = 0

        # Lancer animation
        self.load()

    # ================================
    # 🔄 Animation de chargement
    # ================================
    def load(self):
        if self.progress['value'] < 100:
            self.progress['value'] += 2
            dots = "." * ((self.progress['value'] // 10) % 4)
            self.loading_label.config(text=f"Chargement{dots}")
            self.splash.after(50, self.load)
        else:
            self.open_main()  # <-- fonctionne maintenant
            self.root.attributes('-alpha', 1)

    # ================================
    # 🚀 Ouvrir la fenêtre Login
    # ================================
    def open_main(self):
        # Fermer le splash
        self.splash.destroy()

        # Réafficher la fenêtre principale
        self.root.deiconify()

        # Ouvrir la fenêtre de login
        try:
            from views.login import LoginWindow
            LoginWindow(self.root)
        except Exception as e:
            print("Erreur ouverture login :", e)