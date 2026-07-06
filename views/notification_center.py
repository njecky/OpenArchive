import tkinter as tk
from tkinter import ttk
from config.constants import *
from controllers.notification_controller import *


class NotificationCenter:

    def __init__(self, root):

        self.window = tk.Toplevel(root)
        self.window.title("🔔 Centre de notifications")
        self.window.geometry("900x600")
        self.window.configure(bg=LIGHT_COLOR)

        self.build_ui()
        self.load_data()

    # ================================
    # 🎨 UI
    # ================================
    def build_ui(self):

        title = tk.Label(
            self.window,
            text="🔔 Centre de notifications",
            font=("Arial", 18, "bold"),
            bg=LIGHT_COLOR,
            fg=PRIMARY_COLOR
        )
        title.pack(pady=10)

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # ================================
        # 📌 OVERDUE
        # ================================
        self.frame_overdue = tk.Frame(self.notebook, bg=LIGHT_COLOR)
        self.notebook.add(self.frame_overdue, text="🚨 En retard")

        # ================================
        # ⏰ TODAY
        # ================================
        self.frame_today = tk.Frame(self.notebook, bg=LIGHT_COLOR)
        self.notebook.add(self.frame_today, text="📅 Aujourd'hui")

        # ================================
        # ⚠️ UPCOMING
        # ================================
        self.frame_upcoming = tk.Frame(self.notebook, bg=LIGHT_COLOR)
        self.notebook.add(self.frame_upcoming, text="⏳ À venir")

    # ================================
    # 📊 LOAD DATA
    # ================================
    def load_data(self):

        self.load_list(self.frame_overdue, get_overdue_documents(), "🚨 Alerte retard")
        self.load_list(self.frame_today, get_today_documents(), "📅 À retourner aujourd’hui")
        self.load_list(self.frame_upcoming, get_upcoming_documents(), "⏳ Prochainement")

    # ================================
    # 📋 LIST RENDER
    # ================================
    def load_list(self, frame, data, label_text):

        for widget in frame.winfo_children():
            widget.destroy()

        if not data:
            tk.Label(
                frame,
                text="Aucune notification",
                bg=LIGHT_COLOR
            ).pack(pady=20)
            return

        for row in data:

            card = tk.Frame(frame, bg="white", pady=10, padx=10, relief="groove", bd=1)
            card.pack(fill="x", padx=10, pady=5)

            tk.Label(
                card,
                text=f"📄 {row[1]}",
                font=("Arial", 12, "bold"),
                bg="white"
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"👤 {row[2]}",
                bg="white"
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"📅 Retour prévu : {row[3]} {row[4]}",
                fg="red",
                bg="white"
            ).pack(anchor="w")