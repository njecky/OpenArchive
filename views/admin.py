# ================================
# 👑 ADMIN DASHBOARD - ArchivaDesk (MODERNE UI/UX)
# ================================
import sqlite3
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox, Toplevel, Frame, Label, Button
from config.constants import *
import os
import shutil
import uuid
import subprocess
from datetime import datetime
from models.model import *
from controllers.user_controller import *
from config.function import *
from views.document_viewer import *

try:
    import win32print
    import win32api
    WINDOWS_PRINT = True
except:
    WINDOWS_PRINT = False


class AdminDashboard:

    def __init__(self, root, nom):

        self.root = root
        self.nom = nom

        # ================================
        # 🖥️ WINDOW CONFIG (CENTRÉ + PETIT STYLE SaaS)
        # ================================
        self.root.title(f"{APP_NAME} - Admin Panel")

        width = 1100
        height = 650

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg=LIGHT_COLOR)
        self.root.resizable(False, False)

        # ================================
        # 🧱 MAIN WRAPPER (CARD UI)
        # ================================
        self.wrapper = tk.Frame(self.root, bg=LIGHT_COLOR)
        self.wrapper.pack(fill="both", expand=True, padx=15, pady=15)

        # ================================
        # 📌 SIDEBAR (MODERNE)
        # ================================
        self.sidebar = tk.Frame(
            self.wrapper,
            bg=PRIMARY_COLOR,
            width=220
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # LOGO
        # tk.Label(
        #     self.sidebar,
        #     text="📁 ArchivaDesk",
        #     bg=DARK_COLOR,
        #     fg=WHITE,
        #     font=("Helvetica", 14, "bold"),
        #     pady=20
        # ).pack(fill="x")
        tk.Label(
            self.sidebar,
            text=f"📁 {APP_NAME}",
            bg=DARK_COLOR,
            fg=WHITE,
            font=("Helvetica", 14, "bold"),
            pady=20
        ).pack(fill="x")

        # USER PROFILE
        tk.Label(
            self.sidebar,
            text="👑 Admin",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 12, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            self.sidebar,
            text=nom,
            bg=PRIMARY_COLOR,
            fg=LIGHT_COLOR,
            font=("Helvetica", 10)
        ).pack()

        # ================================
        # MENU
        # ================================
        self.create_menu("🏠 Dashboard", self.show_dashboard)
        self.create_menu("👥 Utilisateurs", self.show_users)
        self.create_menu("📁 Documents", self.show_documents)
        self.create_menu("📊 Activité Documents", self.show_document_logs)

        # 🆕 MODULE DOCUMENTS PHYSIQUES
        self.create_menu("📦 Documents Physiques", self.show_physical_documents)

        self.create_menu("⬆ Upload", self.upload_file)
        self.create_menu("🚪 Logout", self.logout)

        # ================================
        # 📊 CONTENT AREA (CARD STYLE)
        # ================================
        self.content = tk.Frame(
            self.wrapper,
            bg=LIGHT_COLOR
        )

        self.content.pack(side="right", fill="both", expand=True)

        # ================================
        # 🔝 TOPBAR (MODERNE)
        # ================================
        self.topbar = tk.Frame(
            self.content,
            bg=WHITE,
            height=60
        )

        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.page_title = tk.Label(
            self.topbar,
            text="Dashboard",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 16, "bold")
        )

        self.page_title.pack(side="left", padx=20)

        # ================================
        # 📦 BODY
        # ================================
        self.body = tk.Frame(
            self.content,
            bg=LIGHT_COLOR
        )

        self.body.pack(fill="both", expand=True, padx=15, pady=15)

        # DEFAULT VIEW
        self.show_dashboard()

    # ================================
    # 📌 MENU ITEM (MODERNE)
    # ================================
    def create_menu(self, text, command):

        btn = tk.Button(
            self.sidebar,
            text=text,
            bg=PRIMARY_COLOR,
            fg=WHITE,
            bd=0,
            font=("Helvetica", 11),
            anchor="w",
            padx=20,
            pady=12,
            cursor="hand2",
            activebackground=SECONDARY_COLOR,
            activeforeground=WHITE,
            command=command
        )

        btn.pack(fill="x")

        btn.bind("<Enter>", lambda e: btn.config(bg=SECONDARY_COLOR))
        btn.bind("<Leave>", lambda e: btn.config(bg=PRIMARY_COLOR))

    # ================================
    # 🏠 DASHBOARD (CARDS MODERN UI)
    # ================================
    def show_dashboard(self):

        self.clear_body()
        self.page_title.config(text="Dashboard Admin")

        stats = [
            ("👥 Utilisateurs", "25", SECONDARY_COLOR),
            ("📁 Documents", "120", SUCCESS_COLOR),
            ("⬆ Uploads", "40", WARNING_COLOR)
        ]

        container = tk.Frame(self.body, bg=LIGHT_COLOR)
        container.pack(expand=True)

        for title, value, color in stats:

            card = tk.Frame(
                container,
                bg=WHITE,
                width=220,
                height=120
            )

            card.pack(side="left", padx=10, pady=10)
            card.pack_propagate(False)

            # TOP COLOR BAR
            tk.Frame(card, bg=color, height=6).pack(fill="x")

            tk.Label(
                card,
                text=title,
                bg=WHITE,
                fg=TEXT_COLOR,
                font=("Helvetica", 11)
            ).pack(pady=(15, 5))

            tk.Label(
                card,
                text=value,
                bg=WHITE,
                fg=color,
                font=("Helvetica", 26, "bold")
            ).pack()
            
    # ================================
    # 👥 USERS - CRUD + SEARCH (MODERNE UI)
    # ================================
    def show_users(self):

        self.clear_body()
        self.page_title.config(text="Gestion Utilisateurs")

        # ================================
        # 🔝 HEADER BAR (TITLE + SEARCH + ACTION)
        # ================================
        header = tk.Frame(self.body, bg=LIGHT_COLOR)
        header.pack(fill="x", pady=10)

        # TITLE
        tk.Label(
            header,
            text="👥 Liste des utilisateurs",
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            font=("Helvetica", 18, "bold")
        ).pack(side="left")

        # ================================
        # 🔍 SEARCH BAR
        # ================================
        search_frame = tk.Frame(
           header,
           bg=WHITE,
           bd=1,
           relief="solid"
        )
        search_frame.pack(
            side="right",
            padx=5
        )
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=250,
            height=35,
            corner_radius=8,
            border_width=0,
            fg_color=WHITE,
            text_color=TEXT_COLOR,
            placeholder_text="Rechercher un utilisateur...",
            font=("Helvetica", 11)
        )
        
        self.search_entry.pack(
            side="left",
            padx=5,
            pady=5
        )
        # Recherche en temps réel
        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self.search_user()
        )
        search_btn = tk.Button(
            search_frame,
            text="🔍",
            bg=SECONDARY_COLOR,
            fg=WHITE,
            bd=0,
            cursor="hand2",
            font=("Helvetica", 11),
            padx=10,
            command=self.search_user
        )
        
        search_btn.pack(
            side="right",
            padx=5,
            pady=5
        )

        # ================================
        # 🎛 ACTION BUTTONS (CRUD)
        # ================================
        action_frame = tk.Frame(self.body, bg=LIGHT_COLOR)
        action_frame.pack(fill="x", pady=10)

        tk.Button(
            action_frame,
            text="+ Ajouter",
            bg=SUCCESS_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold"),
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.add_user
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="✏ Modifier",
            bg=WARNING_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold"),
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.edit_user
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="🗑 Supprimer",
            bg=DANGER_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold"),
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.delete_user
        ).pack(side="left", padx=5)

        # ================================
        # 📦 TABLE CONTAINER
        # ================================
        table_frame = tk.Frame(self.body, bg=WHITE)
        table_frame.pack(fill="both", expand=True, pady=10)

        # ================================
        # 📋 TABLE
        # ================================
        self.user_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Nom", "Login", "Rôle"),
            show="headings",
            height=15
        )

        for col in ("ID", "Nom", "Login", "Rôle"):
            self.user_table.heading(col, text=col)
            self.user_table.column(col, width=150)

        self.user_table.pack(fill="both", expand=True)
        self.load_users()

    # ================================
    # 🔥 LOAD USERS DATA
    # ================================
    def load_users(self):
        try:
            users = get_users()  # déjà importé en haut
            self.user_table.delete(*self.user_table.get_children())
            
            for user in users:
                self.user_table.insert("", "end", values=user)
        except Exception as e:
            print("❌ Erreur load_users:", e)
        
    # ================================
    # 🔍 SEARCH USER (LINEAR SEARCH)
    # ================================
    def search_user(self):
        # Mot clé
        keyword = self.search_entry.get().strip().lower()

        # ================================
        # 🔄 SI VIDE → RECHARGER USERS
        # ================================
        if keyword == "":
            self.load_users()
            return

        # ================================
        # 🔍 LINEAR SEARCH
        # ================================
        for row in self.user_table.get_children():
            values = self.user_table.item(row)["values"]

            nom = str(values[1]).lower()
            login = str(values[2]).lower()

            # ================================
            # ✅ MATCH
            # ================================
            if keyword in nom or keyword in login:

                self.user_table.reattach(
                    row,
                    "",
                    "end"
                )

            # ================================
            # ❌ NO MATCH
            # ================================
            else:
                self.user_table.detach(row)
    
    # ================================
    # ➕ ADD USER
    # ================================
    def add_user(self):
        # ================================
        # 🪟 POPUP WINDOW
        # ================================
        win = tk.Toplevel(self.root)
        win.title("Ajouter un utilisateur")

        width = 420
        height = 500

        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)

        win.geometry(f"{width}x{height}+{x}+{y}")
        win.configure(bg=LIGHT_COLOR)
        win.resizable(False, False)

        # ================================
        # 📌 TITLE
        # ================================
        tk.Label(
            win,
            text="➕ Nouvel utilisateur",
            font=("Helvetica", 18, "bold"),
            bg=LIGHT_COLOR,
            fg=PRIMARY_COLOR
        ).pack(pady=20)

        # ================================
        # 📦 FORM CONTAINER (CARD)
        # ================================
        form = tk.Frame(
            win,
            bg=WHITE,
            bd=0
        )

        form.pack(padx=20, pady=10, fill="both", expand=True)

        # ================================
        # 🧾 FIELDS
        # ================================
        
        def field(label):
            
            tk.Label(
                form,
                text=label,
                bg=WHITE,
                fg=TEXT_COLOR,
                font=("Helvetica", 10, "bold")
            ).pack(anchor="w", padx=15, pady=(10, 0))
            
            entry = tk.Entry(
                form,
                bd=1,
                relief="solid",
                font=("Helvetica", 11),
                bg=LIGHT_COLOR,
                fg=TEXT_COLOR
            )
            
            entry.pack(fill="x", padx=15, pady=5, ipady=6)
            
            return entry
        name_entry = field("Nom complet")
        login_entry = field("Login")
        password_entry = field("Mot de passe")

        # ================================
        # 🔐 ROLE SELECT
        # ================================
        tk.Label(
            form,
            text="Rôle",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 0))

        role_var = tk.StringVar()
        role_var.set(ROLE_USER)

        role_menu = tk.OptionMenu(form, role_var, *ROLES)
        role_menu.config(
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            highlightthickness=0
        )
        role_menu.pack(fill="x", padx=15, pady=5)

        # ================================
        # 🎛 BUTTONS CONTAINER
        # ================================
        btn_frame = tk.Frame(win, bg=LIGHT_COLOR)
        btn_frame.pack(pady=15)

        # ================================
        # 💾 SAVE BUTTON
        # ================================
        def save_user():
            name = name_entry.get().strip()
            login = login_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get()

            # ================================
            # ❌ VALIDATION
            # ================================
            if name == "" or login == "" or password == "":
                messagebox.showerror(
                    "Erreur",
                    "Tous les champs sont obligatoires"
                )
                return

            # ================================
            # 💾 SAVE DATABASE
            # ================================
            result = add_user_db(
                name,
                login,
                password,
                role
            )

            # ================================
            # ✅ SUCCESS
            # ================================
            if result["success"]:
                messagebox.showinfo(
                    "Succès",
                    result["message"]
                )
                
                win.destroy()
                
                # refresh users table
                try:
                    self.show_users()
                except:
                    pass
                
            # ================================
            # ❌ ERROR
            # ================================
            else:
                messagebox.showerror(
                    "Erreur",
                    result["message"]
                )

        # ================================
        # ❌ CANCEL BUTTON
        # ================================
        def cancel():
            win.destroy()

        # ================================
        # 🟢 BUTTON SAVE
        # ================================
        tk.Button(
            btn_frame,
            text="💾 Enregistrer",
            bg=SUCCESS_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold"),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=save_user
        ).pack(side="left", padx=10)
        
        # ================================
        # 🔴 BUTTON CANCEL
        # ================================
        tk.Button(
            btn_frame,
            text="❌ Annuler",
            bg=DANGER_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold"),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=cancel
        ).pack(side="left", padx=10)
        
    # ================================
    # ✏️ EDIT USER
    # ================================
    def edit_user(self):
        selected = self.user_table.focus()
        
        if not selected:
            messagebox.showwarning(
                "Attention",
                "Sélectionnez un utilisateur"
            )
            return

        # ================================
        # 📦 DATA USER
        # ================================
        data = self.user_table.item(selected)["values"]

        user_id = data[0]
        nom = data[1]
        login = data[2]
        role = data[3]

        # ================================
        # 🪟 POPUP
        # ================================
        popup = tk.Toplevel(self.root)

        popup.title("Modifier utilisateur")

        width = 500
        height = 420

        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        popup.geometry(f"{width}x{height}+{x}+{y}")

        popup.configure(bg=LIGHT_COLOR)
        popup.resizable(False, False)

        popup.grab_set()

        # ================================
        # 🎨 CARD
        # ================================
        card = tk.Frame(
            popup,
            bg=WHITE
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=430,
            height=450
        )

        # ================================
        # 🔝 HEADER
        # ================================
        header = tk.Frame(
            card,
            bg=PRIMARY_COLOR,
            height=70
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="✏ Modifier Utilisateur",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 18, "bold")
        ).pack(pady=18)

        # ================================
        # 📦 FORM
        # ================================
        form = tk.Frame(card, bg=WHITE)
        form.pack(fill="both", expand=True, padx=30, pady=25)

        # ================================
        # 👤 NOM
        # ================================
        tk.Label(
            form,
            text="Nom complet",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w")

        entry_nom = tk.Entry(
            form,
            font=("Helvetica", 11),
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            relief="flat"
        )

        entry_nom.pack(fill="x", ipady=10, pady=5)
        entry_nom.insert(0, nom)

        # ================================
        # 🔐 LOGIN
        # ================================
        tk.Label(
            form,
            text="Login",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", pady=(15, 0))

        entry_login = tk.Entry(
            form,
            font=("Helvetica", 11),
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            relief="flat"
        )

        entry_login.pack(fill="x", ipady=10, pady=5)
        entry_login.insert(0, login)

        # ================================
        # 🛡 ROLE
        # ================================
        tk.Label(
            form,
            text="Rôle",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", pady=(15, 0))

        role_var = tk.StringVar()
        role_var.set(role)

        role_box = ttk.Combobox(
            form,
            textvariable=role_var,
            values=ROLES,
            state="readonly",
            font=("Helvetica", 11)
        )

        role_box.pack(fill="x", ipady=5, pady=5)

        # ================================
        # 💾 UPDATE FUNCTION
        # ================================
        def update_user():
            # import sqlite3
            
            new_nom = entry_nom.get()
            new_login = entry_login.get()
            new_role = role_var.get()

            # ================================
            # ✅ VALIDATION
            # ================================
            if new_nom == "" or new_login == "":

                messagebox.showerror(
                    "Erreur",
                    "Champs obligatoires manquants"
                )
                return
            
            try:
                # ================================
                # 🔌 CONNEXION DB
                # ================================
                conn = sqlite3.connect(DB_PATH)

                cursor = conn.cursor()
                
                # ================================
                # 🔍 RÉCUPÉRER ROLE ID
                # ================================
                cursor.execute(
                    "SELECT id FROM roles WHERE name=?",
                    (new_role,)
                )
                
                role_data = cursor.fetchone()
                
                if not role_data:
                    messagebox.showerror(
                        "Erreur",
                        "Rôle introuvable"
                    )
                    return
                
                role_id = role_data[0]
                
                # ================================
                # 🔥 UPDATE USER
                # ================================
                cursor.execute("""
                        UPDATE users
                        SET nom=?,
                            login=?,
                            role_id=?
                        WHERE id=?
                """, (
                    new_nom,
                    new_login,
                    role_id,
                    user_id
                ))
                
                conn.commit()

                # ================================
                # 🔄 UPDATE TREEVIEW
                # ================================
                self.user_table.item(
                    selected,
                    values=(
                        user_id,
                        new_nom,
                        new_login,
                        new_role
                    )
                )

                # ================================
                # ✅ SUCCESS
                # ================================
                messagebox.showinfo(
                    "Succès",
                    "Utilisateur modifié avec succès"
                )
                
                popup.destroy()

            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    str(e)
                )
            
            finally:
                
                conn.close()

        # ================================
        # 🎛 BUTTONS
        # ================================
        btn_frame = tk.Frame(form, bg=WHITE)
        btn_frame.pack(pady=25)

        # CANCEL
        tk.Button(
            btn_frame,
            text="Annuler",
            bg="#EAECEF",
            fg=TEXT_COLOR,
            bd=0,
            font=("Helvetica", 11),
            padx=20,
            pady=10,
            cursor="hand2",
            command=popup.destroy
        ).pack(side="left", padx=10)

        # SAVE
        save_btn = tk.Button(
            btn_frame,
            text="💾 Enregistrer",
            bg=SECONDARY_COLOR,
            fg=WHITE,
            bd=0,
            font=("Helvetica", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            command=update_user
        )

        save_btn.pack(side="left", padx=10)

        # ================================
        # ✨ HOVER EFFECT
        # ================================
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg=PRIMARY_COLOR))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=SECONDARY_COLOR))
    
    # ================================
    # 🗑️ DELETE USER
    # ================================
    def delete_user(self):
        # ================================
        # 🔍 Vérifier table
        # ================================
        if not hasattr(self, "user_table"):
            messagebox.showerror(
                "Erreur",
                "Table des utilisateurs non chargée"
            )

            return

        # ================================
        # 🎯 USER SELECTED
        # ================================
        selected = self.user_table.focus()

        if not selected:

            messagebox.showwarning(
                "Suppression",
                "Veuillez sélectionner un utilisateur"
            )

            return

        # ================================
        # 📦 DATA USER
        # ================================
        user_data = self.user_table.item(selected)["values"]

        user_id = user_data[0]
        user_name = user_data[1]
        user_role = user_data[3]

        # ================================
        # ⚠️ PROTECTION ADMIN
        # ================================
        if user_role == ROLE_ADMIN:

            messagebox.showwarning(
                "Protection",
                "Impossible de supprimer un administrateur"
            )

            return

        # ================================
        # ⚠️ CONFIRMATION
        # ================================
        confirm = messagebox.askyesno(
            "Confirmation suppression",
            f"Voulez-vous vraiment supprimer :\n\n{user_name} ?"
        )

        if not confirm:
            return

        # ================================
        # 🗄️ DELETE DATABASE
        # ================================
        try:

            # import sqlite3

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # DELETE USER
            cursor.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,)
            )

            conn.commit()
            conn.close()

            # ================================
            # 🖥️ DELETE UI
            # ================================
            self.user_table.delete(selected)

            # SUCCESS MESSAGE
            messagebox.showinfo(
                "Succès",
                f"Utilisateur '{user_name}' supprimé avec succès"
            )

        except Exception as e:

            messagebox.showerror(
                "Erreur suppression",
                str(e)
            )
    # ================================
    # 📁 DOCUMENTS
    # ================================
    def show_documents(self):

        self.clear_body()

        self.page_title.config(
            text="Gestion des documents"
        )

        # ================================
        # 🌟 CONTAINER
        # ================================
        container = tk.Frame(
            self.body,
            bg=LIGHT_COLOR
        )

        container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # ================================
        # 📌 HEADER
        # ================================
        header = tk.Frame(
            container,
            bg=LIGHT_COLOR,
            height=50
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        # LEFT
        left_header = tk.Frame(
            header,
            bg=LIGHT_COLOR
        )

        left_header.pack(side="left")

        title = tk.Label(
            left_header,
            text="📁 Gestion des documents",
            bg=LIGHT_COLOR,
            fg=PRIMARY_COLOR,
            font=("Helvetica", 16, "bold")
        )

        title.pack(anchor="w")
        
        total_documents = count_all_documents()
        subtitle = tk.Label(
            left_header,
            text=f"Système centralisé d'archivage • {total_documents} document(s) • Version {APP_VERSION}",
            bg=LIGHT_COLOR,
            fg="gray",
            font=("Helvetica", 8)
        )

        subtitle.pack(anchor="w")

        # RIGHT
        right_header = tk.Frame(
            header,
            bg=LIGHT_COLOR
        )

        right_header.pack(side="right")

        # Upload button
        upload_btn = tk.Button(
            right_header,
            text="⬆ Importer",
            bg=SECONDARY_COLOR,
            fg=WHITE,
            bd=0,
            font=("Helvetica", 8, "bold"),
            padx=12,
            pady=6,
            cursor="hand2",
            activebackground=PRIMARY_COLOR,
            command=self.upload_file
        )

        upload_btn.pack(side="left", padx=3)

        # Folder button
        folder_btn = tk.Button(
            right_header,
            text="📂 Dossier",
            bg=SUCCESS_COLOR,
            fg=WHITE,
            bd=0,
            font=("Helvetica", 8, "bold"),
            padx=12,
            pady=6,
            cursor="hand2",
            activebackground=PRIMARY_COLOR
        )

        folder_btn.pack(side="left", padx=3)

        # ================================
        # 🔍 SEARCH SECTION
        # ================================
        search_section = tk.Frame(
            container,
            bg=WHITE,
            height=55,
            bd=1,
            relief="solid"
        )

        search_section.pack(
            fill="x",
            pady=(8, 8)
        )

        search_section.pack_propagate(False)

        # Search frame
        search_frame = tk.Frame(
            search_section,
            bg=LIGHT_COLOR
        )

        search_frame.place(
            x=10,
            y=10,
            width=240,
            height=30
        )

        search_icon = tk.Label(
            search_frame,
            text="🔍",
            bg=LIGHT_COLOR,
            font=("Helvetica", 9)
        )

        search_icon.pack(side="left", padx=5)

        self.search_entry = tk.Entry(
            search_frame,
            bd=0,
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            font=("Helvetica", 9)
        )

        self.search_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5)
        )

        self.search_entry.insert(0, "Rechercher...")

        # Category filter
        self.category_combo = ttk.Combobox(
            search_section,
            values=[
                "Catégories",
                "Finance",
                "RH",
                "Contrats",
                "Factures",
                "Archives"
            ],
            state="readonly",
            font=("Helvetica", 8)
        )
        
        self.category_combo.current(0)

        self.category_combo.place(
            x=270,
            y=10,
            width=130,
            height=30
        )

        # Type filter
        self.type_combo = ttk.Combobox(
            search_section,
            values=[
                "Types",
                "PDF",
                "WORD",
                "EXCEL",
                "IMAGE"
            ],
            state="readonly",
            font=("Helvetica", 8)
        )

        self.type_combo.current(0)

        self.type_combo.place(
            x=420,
            y=10,
            width=120,
            height=30
        )
        
        # Recherche en temps réel
        self.search_entry.bind(
            "<KeyRelease>",
            self.search_documents
        )

        # Changement catégorie
        self.category_combo.bind(
            "<<ComboboxSelected>>",
            self.search_documents
        )

        # Changement type
        self.type_combo.bind(
            "<<ComboboxSelected>>",
            self.search_documents
        )
    
        # ================================
        # 📊 STATS
        # ================================
        stats_container = tk.Frame(
            container,
            bg=LIGHT_COLOR
        )

        stats_container.pack(
            fill="x",
            pady=(0, 8)
        )

        stats_frame = tk.Frame(
            stats_container,
            bg=LIGHT_COLOR
        )

        stats_frame.pack(anchor="w")
        
        pdf_count = count_documents_by_type("PDF")
        word_count = count_documents_by_type("WORD")
        excel_count = count_documents_by_type("EXCEL")
        image_count = count_documents_by_type("IMAGE")

        self.create_document_card(
            stats_frame,
            "PDF",
            str(pdf_count),
            DANGER_COLOR
        )

        self.create_document_card(
            stats_frame,
            "WORD",
            str(word_count),
            SECONDARY_COLOR
        )

        self.create_document_card(
            stats_frame,
            "EXCEL",
            str(excel_count),
            WARNING_COLOR
        )

        self.create_document_card(
            stats_frame,
            "IMAGE",
            str(image_count),
            SUCCESS_COLOR
        )

        # ================================
        # 📁 TABLE SECTION
        # ================================
        table_section = tk.Frame(
            container,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        table_section.pack(
            fill="both",
            expand=True
        )

        # ================================
        # 📌 TABLE HEADER
        # ================================
        table_header = tk.Frame(
            table_section,
            bg=WHITE,
            height=40
        )

        table_header.pack(fill="x")
        table_header.pack_propagate(False)

        table_title = tk.Label(
            table_header,
            text="📂 Documents archivés",
            bg=WHITE,
            fg=PRIMARY_COLOR,
            font=("Helvetica", 11, "bold")
        )

        table_title.pack(
            side="left",
            padx=10,
            pady=10
        )

        # ================================
        # 🎨 TABLE STYLE
        # ================================
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT_COLOR,
            rowheight=28,
            fieldbackground=WHITE,
            borderwidth=0,
            font=("Helvetica", 8)
        )

        style.configure(
            "Treeview.Heading",
            background=PRIMARY_COLOR,
            foreground=WHITE,
            relief="flat",
            font=("Helvetica", 8, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", SECONDARY_COLOR)],
            foreground=[("selected", WHITE)]
        )

        # ================================
        # 📋 TABLE
        # ================================
        columns = (
            "Nom",
            "Type",
            "Catégorie",
            "Tags",
            "Taille",
            "Date"
        )

        self.document_table = ttk.Treeview(
            table_section,
            columns=columns,
            show="headings",
            height=9
        )

        # Headings
        for col in columns:

            self.document_table.heading(
                col,
                text=col
            )

        # Columns
        self.document_table.column(
            "Nom",
            width=220
        )

        self.document_table.column(
            "Type",
            width=70,
            anchor="center"
        )

        self.document_table.column(
            "Catégorie",
            width=100,
            anchor="center"
        )

        self.document_table.column(
            "Tags",
            width=120
        )

        self.document_table.column(
            "Taille",
            width=70,
            anchor="center"
        )

        self.document_table.column(
            "Date",
            width=100,
            anchor="center"
        )

        # ================================
        # 📄 DONNÉES
        # ================================
        documents = get_documents()
        
        # Insert data
        self.document_table.delete(*self.document_table.get_children())

        for doc in documents:
            doc_id = doc[0]
            nom = doc[1]
            type_doc = doc[2]
            categorie = doc[3]
            tags = doc[4]
            taille = doc[5]
            date_creation = doc[6]

            icon = (
                "📄" if type_doc == "PDF"
                else "📝" if type_doc == "WORD"
                else "📊" if type_doc == "EXCEL"
                else "🖼"
            )

            self.document_table.insert(
                "",
                "end",
                iid=str(doc_id),  # ID caché
                values=(
                    f"{icon} {nom}",
                    type_doc,
                    categorie,
                    tags,
                    taille,
                    date_creation
                )
            )

        # ================================
        # 🖱️ MENU CONTEXTUEL
        # ================================
        self.doc_menu = tk.Menu(
            self.root,
            tearoff=0,
            bg=WHITE,
            fg=TEXT_COLOR,
            activebackground=SECONDARY_COLOR,
            activeforeground=WHITE,
            font=("Helvetica", 9)
        )
        
        ## Ouvrir
        self.doc_menu.add_command(
            label="📂 Ouvrir  Ctrl+O",
            command=self.open_selected_document
        )
        
        ## Modifier
        self.doc_menu.add_command(
            label="✏ Modifier  Ctrl+E",
            command=self.edit_selected_document
        )

        self.doc_menu.add_separator()
        
        ## Télécharger
        self.doc_menu.add_command(
            label=" Télécharger Ctrl+D",
            command=self.download_selected_document
        )
        
        ## Supprimer
        self.doc_menu.add_command(
            label="🗑 Supprimer Ctrl+Delete",
            command=self.delete_selected_document
        )
        
        self.doc_menu.add_separator()
        ## Imprimer
        self.doc_menu.add_command(
            label="🖨 Imprimer Ctrl+P",
            command=self.print_selected_document
        )
        
        # ================================
        # 🖱️ RIGHT CLICK
        # ================================
        self.document_table.bind(
            "<Button-3>",
            self.show_document_menu
        )

        # ================================
        # ⌨️ RACCOURCIS CLAVIER
        # ================================
        self.root.bind(
            "<Control-o>",
            lambda e: self.open_selected_document()
        )

        self.root.bind(
            "<Control-e>",
            lambda e: self.edit_selected_document()
        )
        
        self.root.bind(
            "<Control-d>",
            lambda event: self.download_selected_document()
        )

        self.root.bind(
            "<Control-Delete>",
            lambda e: self.delete_selected_document()
        )

        self.root.bind(
            "<Double-1>",
            lambda e: self.open_selected_document()
        )
        
        self.root.bind(
            "<Control-p>",
            lambda e: self.print_selected_document()
        )
        
        # ================================
        # 📜 SCROLLBAR
        # ================================
        scrollbar = ttk.Scrollbar(
            table_section,
            orient="vertical",
            command=self.document_table.yview
        )

        self.document_table.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.document_table.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 5)
        )

        # ================================
        # 📌 FOOTER
        # ================================
        footer = tk.Frame(
            container,
            bg="red",
            height=50
        )

        footer.pack(fill="x",side="bottom")

        footer.pack_propagate(False)
        
        total_documents = count_all_documents()
        footer_label = tk.Label(
            footer,
            text=f"{total_documents} document(s) archivé(s) • ArchivaDesk",
            bg=LIGHT_COLOR,
            fg="gray",
            font=("Helvetica", 8)
        )

        footer_label.pack(
            side="left",
            pady=5
        )

    # ================================
    # 🔍 RECHERCHE DOCUMENTS
    # ================================
    def search_documents(self, event=None):

        keyword = self.search_entry.get().strip().lower()
        category = self.category_combo.get()
        doc_type = self.type_combo.get()

        if keyword == "rechercher...":
            keyword = ""

        documents = get_documents()

        self.document_table.delete(*self.document_table.get_children())

        result_count = 0

        # ================================
        # 🔍 LINEAR SEARCH
        # ================================
        for doc in documents:

            doc_id = doc[0]
            nom = doc[1]
            type_document = doc[2]
            categorie = doc[3]
            tags = doc[4]
            taille = doc[5]
            date_creation = doc[6]

            # ------------------------
            # Recherche texte
            # ------------------------
            found_keyword = True

            if keyword:
                found_keyword = (
                    keyword in str(nom).lower()
                    or keyword in str(tags).lower()
                    or keyword in str(categorie).lower()
                    or keyword in str(type_document).lower()
                )

            # ------------------------
            # Filtre catégorie
            # ------------------------
            found_category = True

            if category != "Catégories":
                found_category = (
                    categorie.lower() == category.lower()
                )

            # ------------------------
            # Filtre type
            # ------------------------
            found_type = True

            if doc_type != "Types":
                found_type = (
                    type_document.lower() == doc_type.lower()
                )

            # ------------------------
            # MATCH FINAL
            # ------------------------
            if found_keyword and found_category and found_type:

                result_count += 1

                icon = (
                    "📄" if type_document == "PDF"
                    else "📝" if type_document == "WORD"
                    else "📊" if type_document == "EXCEL"
                    else "🖼"
                )

                self.document_table.insert(
                    "",
                    "end",
                    iid=str(doc_id),
                    values=(
                        f"{icon} {nom}",
                        type_document,
                        categorie,
                        tags,
                        taille,
                        date_creation
                    )
                )

        # ================================
        # 📌 UPDATE TITLE
        # ================================
        self.page_title.config(
            text=f"Gestion des documents ({result_count} résultat(s))"
        )
    # ================================
    # 🖱️ AFFICHER MENU CONTEXTUEL
    # ================================
    def show_document_menu(self, event):

        selected = self.document_table.identify_row(
            event.y
        )

        if selected:

            self.document_table.selection_set(
                selected
            )

            self.doc_menu.post(
                event.x_root,
                event.y_root
            )


    # ================================
    # 📂 OUVRIR DOCUMENT
    # ================================
    def open_selected_document(self):

        selected = self.document_table.selection()

        if not selected:

            messagebox.showwarning(
                "Document",
                "Veuillez sélectionner un document."
            )

            return

        try:

            # ================================
            # 📄 ID DOCUMENT
            # ================================
            document_id = int(selected[0])

            # ================================
            # 🔍 RÉCUPÉRATION DOCUMENT
            # ================================
            document = get_document_by_id(
                document_id
            )

            if not document:

                messagebox.showerror(
                    "Erreur",
                    "Document introuvable."
                )

                return

            # ================================
            # 📄 DONNÉES DOCUMENT
            # ================================
            document_name = document[1]

            document_path = document[6]

            # ================================
            # 📝 JOURNAL ACTIVITÉ
            # ================================
            try:

                add_document_activity(

                    document_id=document_id,

                    document_name=document_name,

                    user_id=1,

                    action="Consultation",

                    ip_address=get_public_ip()

                )

            except Exception as log_error:

                print(
                    f"Erreur journal activité : {log_error}"
                )

            # ================================
            # 📂 OUVERTURE DOCUMENT
            # ================================
            DocumentViewer(

                self.root,

                document_name,

                document_path

            )

        except Exception as e:

            messagebox.showerror(
                "Erreur",
                str(e)
        )
    # ================================
    # 📂 OUVRIR / TÉLÉCHARGER DOCUMENT
    # ================================
    def download_selected_document(self):

        selected = self.document_table.selection()

        if not selected:
            messagebox.showwarning(
                "Téléchargement",
                "Veuillez sélectionner un document."
            )
            return

        try:

            # ================================
            # 📄 ID DOCUMENT
            # ================================
            document_id = int(selected[0])

            document = get_document_by_id(document_id)

            if not document:
                messagebox.showerror(
                    "Erreur",
                    "Document introuvable dans la base de données."
                )
                return

            document_name = document[1]
            source_path = document[6]

            # ================================
            # 📂 VÉRIFIER FICHIER
            # ================================
            if not os.path.exists(source_path):
                messagebox.showerror(
                    "Erreur",
                    f"Fichier introuvable :\n{source_path}"
                )
                return

            # ================================
            # 📁 DOSSIER TÉLÉCHARGEMENTS
            # ================================
            target_folder = os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            )

            if not os.path.exists(target_folder):

                target_folder = filedialog.askdirectory(
                    title="Choisir un dossier"
                )

                if not target_folder:
                    return

            # ================================
            # 📄 NOM FICHIER
            # ================================
            clean_name = document_name.strip()

            base, ext = os.path.splitext(clean_name)

            destination = os.path.join(
                target_folder,
                clean_name
            )

            # ================================
            # 🔁 GESTION DOUBLONS
            # ================================
            counter = 1

            while os.path.exists(destination):

                destination = os.path.join(
                    target_folder,
                    f"{base}_{counter}{ext}"
                )

                counter += 1

            # ================================
            # 📦 COPIE FICHIER
            # ================================
            shutil.copy2(
                source_path,
                destination
            )

            # ================================
            # 🌍 IP PUBLIQUE
            # ================================
            ip_address = get_public_ip()

            # ================================
            # 👤 UTILISATEUR CONNECTÉ
            # ================================
            user_id = 1

            # Exemple :
            # user_id = self.current_user_id

            # ================================
            # 📝 JOURNAL ACTIVITÉ
            # ================================
            add_document_activity(
                document_id=document_id,

                document_name=document_name,

                user_id=1,

                action="Téléchargement",

                ip_address=ip_address
            )
            # ================================
            # ✅ SUCCÈS
            # ================================
            messagebox.showinfo(
                "Téléchargement réussi",
                f"Document téléchargé avec succès :\n\n{destination}"
            )

        except PermissionError:

            messagebox.showerror(
                "Accès refusé",
                "Vous n'avez pas les permissions nécessaires."
            )

        except Exception as e:

            messagebox.showerror(
                "Erreur",
                str(e)
            )
    # ================================
    # ✏ MODIFIER DOCUMENT
    # ================================
    def edit_selected_document(self):

        selected = self.document_table.selection()

        if not selected:
            messagebox.showwarning(
                "Modifier",
                "Veuillez sélectionner un document."
            )
            return

        try:
            # ================================
            # 📄 ID DOCUMENT
            # ================================
            document_id = int(selected[0])

            document = get_document_by_id(document_id)

            if not document:
                messagebox.showerror("Erreur", "Document introuvable.")
                return

            # ================================
            # 📦 DATA
            # ================================
            doc_id = document[0]
            nom = document[1]
            type_doc = document[2]
            categorie = document[3]
            tags = document[4]
            taille = document[5]
            chemin = document[6]

            old_category = categorie
            old_path = chemin

            # ================================
            # 🪟 WINDOW
            # ================================
            window = tk.Toplevel(self.root)
            window.title("Modifier document")
            window.geometry("600x520")
            window.configure(bg=LIGHT_COLOR)
            window.grab_set()

            # ================================
            # 🧱 HEADER
            # ================================
            header = tk.Frame(window, bg=PRIMARY_COLOR, height=70)
            header.pack(fill="x")
            header.pack_propagate(False)

            tk.Label(
                header,
                text="✏ Modifier le document",
                bg=PRIMARY_COLOR,
                fg=WHITE,
                font=("Helvetica", 16, "bold")
            ).pack(side="left", padx=20, pady=20)

            # ================================
            # 📦 BODY CARD
            # ================================
            card = tk.Frame(window, bg=WHITE)
            card.pack(fill="both", expand=True, padx=20, pady=20)

            # ================================
            # 📝 NOM
            # ================================
            tk.Label(card, text="Nom du document", bg=WHITE, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=(15, 5))

            nom_entry = tk.Entry(card, font=("Helvetica", 11))
            nom_entry.pack(fill="x", padx=20)
            nom_entry.insert(0, nom)

            # ================================
            # 📂 CATÉGORIE
            # ================================
            tk.Label(card, text="Catégorie", bg=WHITE, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=(15, 5))

            categorie_combo = ttk.Combobox(
                card,
                values=["Finance", "RH", "Contrats", "Factures", "Archives"],
                state="readonly",
                font=("Helvetica", 11)
            )
            categorie_combo.pack(fill="x", padx=20)
            categorie_combo.set(categorie)

            # ================================
            # 🏷 TAGS
            # ================================
            tk.Label(card, text="Tags", bg=WHITE, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=(15, 5))

            tags_entry = tk.Entry(card, font=("Helvetica", 11))
            tags_entry.pack(fill="x", padx=20)
            tags_entry.insert(0, tags)

            # ================================
            # 📊 INFO
            # ================================
            info = tk.Label(
                card,
                text=f"📄 Type: {type_doc}   |   📏 Taille: {taille}",
                bg=WHITE,
                fg="gray"
            )
            info.pack(anchor="w", padx=20, pady=15)

            # ================================
            # 🔘 FOOTER BUTTONS
            # ================================
            footer = tk.Frame(card, bg=WHITE)
            footer.pack(fill="x", pady=20)

            # ❌ ANNULER
            def cancel():
                window.destroy()

            cancel_btn = tk.Button(
                footer,
                text="❌ Annuler",
                bg=DANGER_COLOR,
                fg=WHITE,
                font=("Helvetica", 10, "bold"),
                padx=15,
                pady=8,
                command=cancel
            )
            cancel_btn.pack(side="right", padx=10)

            # ================================
            # 💾 SAUVEGARDER
            # ================================
            def save():

                new_nom = nom_entry.get().strip()
                new_cat = categorie_combo.get().strip()
                new_tags = tags_entry.get().strip()

                if not new_nom:
                    messagebox.showerror("Erreur", "Nom obligatoire")
                    return

                try:
                    new_path = old_path

                    # ================================
                    # 📁 CHANGEMENT DE CATÉGORIE
                    # ================================
                    if new_cat != old_category:

                        category_folder = os.path.join(
                            ARCHIVE_PATH,
                            new_cat
                        )

                        if not os.path.exists(category_folder):
                            os.makedirs(category_folder)

                        filename = os.path.basename(old_path)

                        new_path = os.path.join(category_folder, filename)

                        shutil.move(old_path, new_path)

                    # ================================
                    # 💾 UPDATE DB
                    # ================================
                    conn = connect_db()
                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE documents
                        SET nom = ?, categorie = ?, tags = ?, chemin = ?
                        WHERE id = ?
                    """, (
                        new_nom,
                        new_cat,
                        new_tags,
                        new_path,
                        doc_id
                    ))

                    conn.commit()
                    conn.close()
                    
                    # ================================
                    # 📝 ENREGISTRER L'ACTIVITÉ
                    # ================================
                    try:
                        user_id = self.current_user["id"]
                    except:
                        user_id = 1
                        
                    add_document_activity(
                        document_id=doc_id,
                        document_name=new_nom,
                        user_id=user_id,
                        action="Modification",
                        ip_address=get_public_ip()
                    )
                    messagebox.showinfo(
                        "Succès",
                        "Document modifié avec succès"
                    )

                    window.destroy()
                    self.show_documents()

                except Exception as e:
                    messagebox.showerror("Erreur", str(e))

            # ================================
            # 💾 BOUTON SAUVEGARDER
            # ================================
            save_btn = tk.Button(
                footer,
                text="💾 Sauvegarder les modifications",
                bg=SUCCESS_COLOR,
                fg=WHITE,
                font=("Helvetica", 10, "bold"),
                padx=15,
                pady=8,
                command=save
            )
            save_btn.pack(side="right", padx=10)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    # ================================
    # 🗑 SUPPRIMER DOCUMENT
    # ================================
    def delete_selected_document(self):

        selected = self.document_table.selection()

        if not selected:

            messagebox.showwarning(
                "Suppression",
                "Veuillez sélectionner un document."
            )

            return

        try:

            # ================================
            # 📄 ID DOCUMENT
            # ================================
            document_id = int(selected[0])

            # ================================
            # 📄 DOCUMENT DB
            # ================================
            document = get_document_by_id(document_id)

            if not document:

                messagebox.showerror(
                    "Erreur",
                    "Document introuvable."
                )

                return

            document_name = document[1]

            # ================================
            # ❓ CONFIRMATION
            # ================================
            confirm = messagebox.askyesno(
                "Suppression",
                f"Voulez-vous supprimer :\n\n{document_name} ?"
            )

            if not confirm:
                return

            # ================================
            # 🌍 IP UTILISATEUR
            # ================================
            ip_address = get_public_ip()

            # ================================
            # 📝 AJOUT LOG ACTIVITÉ
            # ================================
            add_document_activity(

                document_id=document_id,

                document_name=document_name,

                user_id=1,  # utilisateur connecté

                action="Suppression",

                ip_address=ip_address

            )

            # ================================
            # 🗃️ SUPPRESSION DB
            # ================================
            file_path = delete_document_by_id(
                document_id
            )

            if not file_path:

                messagebox.showerror(
                    "Erreur",
                    "Document introuvable dans la base."
                )

                return

            # ================================
            # 📁 SUPPRESSION PHYSIQUE
            # ================================
            if os.path.exists(file_path):

                os.remove(file_path)

            # ================================
            # ✅ SUCCÈS
            # ================================
            messagebox.showinfo(
                "Succès",
                "Document supprimé avec succès."
            )

            # ================================
            # 🔄 RECHARGEMENT
            # ================================
            self.show_documents()

        except Exception as e:

            messagebox.showerror(
                "Erreur",
                str(e)
            )
    # ================================
    # 🖨 IMPRIMER DOCUMENT
    # ================================
    def print_selected_document(self):
        selected = self.document_table.selection()

        if not selected:
            messagebox.showwarning(
                "Impression",
                "Veuillez sélectionner un document."
            )
            return

        try:
            # ================================
            # 📄 ID DOCUMENT
            # ================================
            document_id = int(selected[0])

            document = get_document_by_id(document_id)

            if not document:
                messagebox.showerror("Erreur", "Document introuvable.")
                return

            document_name = document[1]
            source_path = document[6]

            if not os.path.exists(source_path):
                messagebox.showerror(
                    "Erreur",
                    f"Fichier introuvable :\n{source_path}"
                )
                return

            # ================================
            # 🪟 FENÊTRE MODERNE
            # ================================
            win = tk.Toplevel(self.root)
            win.title("Aperçu impression - ArchivaDesk")
            win.geometry("700x520")
            win.configure(bg=LIGHT_COLOR)
            win.grab_set()

            # ================================
            # 📌 HEADER
            # ================================
            header = tk.Frame(win, bg=PRIMARY_COLOR, height=70)
            header.pack(fill="x")
            header.pack_propagate(False)

            tk.Label(
                header,
                text="🖨 Aperçu & Impression",
                bg=PRIMARY_COLOR,
                fg=WHITE,
                font=("Helvetica", 16, "bold")
            ).pack(side="left", padx=20)

            # ================================
            # 📦 BODY
            # ================================
            body = tk.Frame(win, bg=LIGHT_COLOR)
            body.pack(fill="both", expand=True, padx=20, pady=20)

            # ================================
            # 📄 INFO DOCUMENT
            # ================================
            card = tk.Frame(body, bg=WHITE, bd=1, relief="solid")
            card.pack(fill="both", expand=True)

            tk.Label(
                card,
                text="📄 Informations du document",
                bg=WHITE,
                fg=PRIMARY_COLOR,
                font=("Helvetica", 13, "bold")
            ).pack(anchor="w", padx=15, pady=10)

            tk.Label(
                card,
                text=f"Nom : {document_name}",
                bg=WHITE,
                fg=TEXT_COLOR,
                font=("Helvetica", 10, "bold")
            ).pack(anchor="w", padx=15)

            tk.Label(
                card,
                text=f"Chemin : {source_path}",
                bg=WHITE,
                fg="gray",
                wraplength=600,
                font=("Helvetica", 9)
            ).pack(anchor="w", padx=15, pady=(5, 10))

            # ================================
            # 🖨 IMPRIMANTE
            # ================================
            tk.Label(
                card,
                text="🖨 Imprimante disponible",
                bg=WHITE,
                fg=TEXT_COLOR,
                font=("Helvetica", 10, "bold")
            ).pack(anchor="w", padx=15)

            printers = []

            if WINDOWS_PRINT:
                printers = [p[2] for p in win32print.EnumPrinters(2)]

            printer_combo = ttk.Combobox(
                card,
                values=printers,
                state="readonly"
            )

            printer_combo.pack(fill="x", padx=15, pady=8)

            if printers:
                printer_combo.current(0)

            # ================================
            # 🔘 FOOTER
            # ================================
            footer = tk.Frame(card, bg=WHITE)
            footer.pack(fill="x", pady=15)

            # ================================
            # ❌ ANNULER
            # ================================
            def cancel():
                win.destroy()

            tk.Button(
                footer,
                text="❌ Annuler",
                bg=DANGER_COLOR,
                fg=WHITE,
                font=("Helvetica", 10, "bold"),
                command=cancel
            ).pack(side="right", padx=5)

            # ================================
            # ⬇ TÉLÉCHARGER (APPEL DIRECT)
            # ================================
            def download():
                win.destroy()
                self.download_selected_document()

            tk.Button(
                footer,
                text="⬇ Télécharger",
                bg=WARNING_COLOR,
                fg=WHITE,
                font=("Helvetica", 10, "bold"),
                command=download
            ).pack(side="right", padx=5)

            # ================================
            # 🖨 IMPRIMER
            # ================================
            def do_print():
                try:
                    printer = printer_combo.get()

                    if not printer:
                        messagebox.showerror("Erreur", "Sélectionnez une imprimante")
                        return

                    if WINDOWS_PRINT:
                        win32api.ShellExecute(
                            0,
                            "print",
                            source_path,
                            f'/d:"{printer}"',
                            ".",
                            0
                        )
                    else:
                        subprocess.run(["lp", "-d", printer, source_path])

                    messagebox.showinfo(
                        "Succès",
                        "Document envoyé à l'imprimante"
                    )

                    win.destroy()

                except Exception as e:
                    messagebox.showerror("Erreur impression", str(e))

            tk.Button(
                footer,
                text="🖨 Imprimer",
                bg=SUCCESS_COLOR,
                fg=WHITE,
                font=("Helvetica", 10, "bold"),
                command=do_print
            ).pack(side="right", padx=5)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ================================
    # 📊 DOCUMENT CARD COMPACT
    # ================================
    def create_document_card(
        self,
        parent,
        title,
        value,
        color
    ):

        CARD_WIDTH = 135
        CARD_HEIGHT = 70

        card = tk.Frame(
            parent,
            bg=WHITE,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            bd=1,
            relief="solid"
        )

        card.pack(
            side="left",
            padx=4,
            pady=2
        )

        card.pack_propagate(False)

        # TOP BAR
        top = tk.Frame(
            card,
            bg=color,
            height=4
        )

        top.pack(fill="x")

        # CONTENT
        content = tk.Frame(
            card,
            bg=WHITE
        )

        content.pack(
            expand=True,
            fill="both"
        )

        # TITLE
        title_label = tk.Label(
            content,
            text=title,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 8),
            width=12,
            anchor="center"
        )

        title_label.pack(
            pady=(6, 1)
        )

        # VALUE
        value_label = tk.Label(
            content,
            text=value,
            bg=WHITE,
            fg=color,
            font=("Helvetica", 14, "bold"),
            width=8,
            anchor="center"
        )

        value_label.pack()
    # ================================
    # ⬆ UPLOAD
    # ================================
    def upload_file(self):
        
        # ================================
        # 📂 CHOISIR DOCUMENT
        # ================================
        filepath = filedialog.askopenfilename(

            title="Sélectionner un document",

            filetypes=[

                ("PDF", "*.pdf"),
                ("Word", "*.docx"),
                ("Excel", "*.xlsx"),
                ("Images", "*.png *.jpg *.jpeg"),
                ("Tous les fichiers", "*.*")

            ]
        )

        # ================================
        # ❌ AUCUN FICHIER
        # ================================
        if not filepath:
            return

        # ================================
        # 📄 INFOS FICHIER
        # ================================
        filename = os.path.basename(filepath)

        extension = os.path.splitext(filename)[1].lower()

        size = round(
            os.path.getsize(filepath) / (1024 * 1024),
            2
        )

        file_size = f"{size} MB"

        # ================================
        # 📄 TYPE
        # ================================
        if extension == ".pdf":
            file_type = "PDF"

        elif extension == ".docx":
            file_type = "WORD"

        elif extension == ".xlsx":
            file_type = "EXCEL"

        elif extension in [".png", ".jpg", ".jpeg"]:
            file_type = "IMAGE"

        else:
            file_type = "AUTRE"

        # ================================
        # 🪟 FENÊTRE MODERNE
        # ================================
        window = tk.Toplevel(self.root)

        window.title("Archiver un document")

        width = 650
        height = 580

        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

        window.configure(bg=LIGHT_COLOR)

        window.resizable(False, False)

        window.grab_set()

        # ================================
        # 📌 HEADER
        # ================================
        header = tk.Frame(
            window,
            bg=PRIMARY_COLOR,
            height=70
        )

        header.pack(fill="x")

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="📁 Archiver un nouveau document",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 16, "bold")
        )

        title.pack(
            side="left",
            padx=20,
            pady=20
        )

        # ================================
        # 📦 BODY
        # ================================
        body = tk.Frame(
            window,
            bg=LIGHT_COLOR
        )

        body.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # ================================
        # 📄 CARD INFO
        # ================================
        card = tk.Frame(
            body,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        card.pack(fill="both", expand=True)

        # ================================
        # 📝 SECTION TITLE
        # ================================
        section_title = tk.Label(
            card,
            text="Informations du document",
            bg=WHITE,
            fg=PRIMARY_COLOR,
            font=("Helvetica", 13, "bold")
        )

        section_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        # ================================
        # 📝 NOM DOCUMENT
        # ================================
        tk.Label(
            card,
            text="Nom du document",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", padx=20)

        nom_entry = tk.Entry(
            card,
            font=("Helvetica", 10),
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            relief="flat"
        )

        nom_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=8
        )

        nom_entry.insert(0, filename)

        # ================================
        # 📄 TYPE + 📂 CATEGORIE
        # ================================
        row1 = tk.Frame(
            card,
            bg=WHITE
        )

        row1.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # TYPE
        left = tk.Frame(
            row1,
            bg=WHITE
        )

        left.pack(side="left", fill="x", expand=True)

        tk.Label(
            left,
            text="Type",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w")

        type_combo = ttk.Combobox(
            left,
            state="readonly",
            values=[
                "PDF",
                "WORD",
                "EXCEL",
                "IMAGE"
            ],
            font=("Helvetica", 10)
        )

        type_combo.pack(
            fill="x",
            pady=(5, 0),
            ipady=4
        )

        type_combo.set(file_type)

        # CATEGORIE
        right = tk.Frame(
            row1,
            bg=WHITE
        )

        right.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 0)
        )

        tk.Label(
            right,
            text="Catégorie",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w")

        categorie_combo = ttk.Combobox(
            right,
            values=[
                "Finance",
                "RH",
                "Contrats",
                "Factures",
                "Archives"
            ],
            font=("Helvetica", 10)
        )

        categorie_combo.pack(
            fill="x",
            pady=(5, 0),
            ipady=4
        )

        # ================================
        # 🏷️ TAGS
        # ================================
        tk.Label(
            card,
            text="Tags",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", padx=20)

        tags_entry = tk.Entry(
            card,
            font=("Helvetica", 10),
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            relief="flat"
        )

        tags_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=8
        )

        tags_entry.insert(0, "#document")

        # ================================
        # 📏 INFOS FICHIER
        # ================================
        info_frame = tk.Frame(
            card,
            bg=LIGHT_COLOR
        )

        info_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        tk.Label(
            info_frame,
            text=f"📄 Type : {file_type}",
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            font=("Helvetica", 9)
        ).pack(anchor="w", padx=10, pady=4)

        tk.Label(
            info_frame,
            text=f"📏 Taille : {file_size}",
            bg=LIGHT_COLOR,
            fg=TEXT_COLOR,
            font=("Helvetica", 9)
        ).pack(anchor="w", padx=10, pady=4)

        tk.Label(
            info_frame,
            text=f"📂 Chemin : {filepath}",
            bg=LIGHT_COLOR,
            fg="gray",
            wraplength=540,
            justify="left",
            font=("Helvetica", 8)
        ).pack(anchor="w", padx=10, pady=4)

        # ================================
        # 🔘 FOOTER BUTTONS
        # ================================
        footer = tk.Frame(
            card,
            bg=WHITE,
            height=80
        )

        footer.pack(
            fill="x",
            pady=(10, 0)
        )

        footer.pack_propagate(False)

        # ================================
        # ❌ ANNULER
        # ================================
        cancel_btn = tk.Button(
            footer,
            text="✖ Annuler",
            bg=DANGER_COLOR,
            fg=WHITE,
            bd=0,
            font=("Helvetica", 10, "bold"),
            padx=18,
            pady=10,
            cursor="hand2",
            activebackground=DARK_COLOR,
            command=window.destroy
        )

        cancel_btn.pack(
            side="right",
            padx=(0, 20),
            pady=18
        )
        
        # ================================
        # 💾 ARCHIVER
        # ================================
        def save_document():

            nom = nom_entry.get().strip()

            categorie = categorie_combo.get().strip()

            tags = tags_entry.get().strip()

            type_doc = type_combo.get()

            # ================================
            # ❌ VALIDATION
            # ================================
            if nom == "":

                messagebox.showerror(
                    "Erreur",
                    "Le nom du document est obligatoire."
                )

                return

            if categorie == "":

                messagebox.showerror(
                    "Erreur",
                    "Veuillez sélectionner une catégorie."
                )

                return

            # ================================
            # 📄 EXTENSION
            # ================================
            extension = os.path.splitext(filepath)[1].lower()

            # ================================
            # 🧹 SÉCURISER LE NOM
            # ================================
            caracteres_interdits = [
                "/", "\\", ":", "*",
                "?", '"', "<", ">", "|"
            ]

            for caractere in caracteres_interdits:

                nom = nom.replace(caractere, "_")

            # ================================
            # 📁 DOSSIER ARCHIVES
            # ================================
            if not os.path.exists(ARCHIVE_PATH):

                os.makedirs(ARCHIVE_PATH)

            # ================================
            # 📂 DOSSIER CATÉGORIE
            # ================================
            categorie_folder = os.path.join(
                ARCHIVE_PATH,
                categorie
            )

            # création uniquement si absent
            if not os.path.exists(categorie_folder):

                os.makedirs(categorie_folder)

            # ================================
            # 🔐 NOM UNIQUE FICHIER
            # ================================
            unique_id = uuid.uuid4().hex[:10]

            final_filename = f"{unique_id}{extension}"

            # ================================
            # 📂 CHEMIN FINAL
            # ================================
            destination = os.path.join(
                categorie_folder,
                final_filename
            )

            # ================================
            # 📄 COPIE FICHIER
            # ================================
            try:

                shutil.copy(
                    filepath,
                    destination
                )

            except Exception as e:

                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'archiver le document.\n\n{e}"
                )

                return

            # ================================
            # 💾 SAVE DATABASE
            # ================================
            try:
                conn = connect_db()

                cursor = conn.cursor()

                cursor.execute("""

                    INSERT INTO documents(

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

                    nom + extension,
                    type_doc,
                    categorie,
                    tags,
                    file_size,
                    destination,
                    1

                ))

                conn.commit()

                conn.close()

            except Exception as e:

                messagebox.showerror(
                    "Erreur Base de données",
                    str(e)
                )

                return

            # ================================
            # ✅ SUCCESS
            # ================================
            messagebox.showinfo(
                "Succès",
                "Document archivé avec succès."
            )

            window.destroy()

            # ================================
            # 🔄 RELOAD
            # ================================
            self.show_documents()
        
        # ================================
        # 💾 BOUTON ARCHIVER
        # ================================
        save_btn = tk.Button(
            footer,
            text="💾 Archiver",
            bg=SUCCESS_COLOR,
            fg=WHITE,
            bd=0,
            font=("Helvetica", 10, "bold"),
            padx=18,
            pady=10,
            cursor="hand2",
            activebackground=PRIMARY_COLOR,
            command=save_document
        )

        save_btn.pack(
            side="right",
            padx=10,
            pady=18
        )
            
    # ================================
    # 📊 DOCUMENT CARD
    # ================================
    def create_document_card(self, parent, title, value, color):
        
        card = tk.Frame(
            parent,
            bg=WHITE,
            width=220,
            height=100
        )

        card.pack(side="left", padx=10)

        card.pack_propagate(False)

        # Top border
        top = tk.Frame(
            card,
            bg=color,
            height=6
        )

        top.pack(fill="x")

        # Title
        title_label = tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 11)
        )

        title_label.pack(pady=(15, 5))

        # Value
        value_label = tk.Label(
            card,
            text=value,
            bg=WHITE,
            fg=color,
            font=("Helvetica", 22, "bold")
        )

        value_label.pack()
    # ================================
    # 🚪 LOGOUT
    # ================================
    def logout(self):

        if messagebox.askyesno("Logout", "Voulez-vous quitter ?"):
            self.root.destroy()

    # ================================
    # 🧹 CLEAR BODY
    # ================================
    def clear_body(self):

        for widget in self.body.winfo_children():
            widget.destroy()
    
    
    
    # ================================
    # 📊 ACTIVITÉ DOCUMENTS (LOGS)
    # ================================
    def show_document_logs(self):

        self.clear_body()

        self.page_title.config(
            text="📊 Activité des documents"
        )

        # ================================
        # 🌟 CONTAINER
        # ================================
        container = tk.Frame(
            self.body,
            bg=LIGHT_COLOR
        )

        container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ================================
        # 📌 HEADER
        # ================================
        header = tk.Frame(
            container,
            bg=LIGHT_COLOR
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="📊 Journal des activités",
            bg=LIGHT_COLOR,
            fg=PRIMARY_COLOR,
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Historique complet des actions effectuées sur les documents",
            bg=LIGHT_COLOR,
            fg="gray",
            font=("Helvetica", 9)
        ).pack(anchor="w")

        # ================================
        # 📊 STATISTIQUES
        # ================================
        downloads = count_downloads()
        edits = count_edits()
        deletes = count_deletes()
        active_users = count_active_users()
        views = count_views()
        
        stats_frame = tk.Frame(
            container,
            bg=LIGHT_COLOR
        )

        stats_frame.pack(
            fill="x",
            pady=(10, 10)
        )
        self._log_card(
            stats_frame,
            "👁 Consultations",
            str(views),
            PRIMARY_COLOR
        )
        self._log_card(
            stats_frame,
            "⬇ Téléchargements",
            str(downloads),
            SECONDARY_COLOR
        )

        self._log_card(
            stats_frame,
            "✏ Modifications",
            str(edits),
            WARNING_COLOR
        )

        self._log_card(
            stats_frame,
            "🗑 Suppressions",
            str(deletes),
            DANGER_COLOR
        )

        self._log_card(
            stats_frame,
            "👥 Utilisateurs",
            str(active_users),
            SUCCESS_COLOR
        )

        # ================================
        # 🔎 FILTRES
        # ================================
        filter_frame = tk.Frame(
            container,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        filter_frame.pack(
            fill="x",
            pady=(0, 10)
        )
        
        # ================================
        # 🔎 FILTRE + RECHERCHE ACTIVITÉS
        # ================================
        tk.Label(
            filter_frame,
            text="🔎 Recherche",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 9, "bold")
        ).pack(
            side="left",
            padx=(10, 5),
            pady=10
        )
        
        # ================================
        # 🔎 ENTRY RECHERCHE
        # ================================
        search_entry = tk.Entry(
            filter_frame,
            font=("Helvetica", 9),
            width=30
        )

        search_entry.pack(
            side="left",
            padx=5
        )
        action_filter = ttk.Combobox(
            filter_frame,
            values=[
                "Toutes",
                "Téléchargement",
                "Modification",
                "Suppression",
                "Consultation"
            ],
            width=18,
            state="readonly"
        )

        action_filter.pack(
            side="left",
            padx=10
        )

        action_filter.set("Toutes")

        tk.Button(
            filter_frame,
            text="🔄 Actualiser",
            bg=SECONDARY_COLOR,
            fg=WHITE,
            bd=0,
            padx=10
        ).pack(
            side="right",
            padx=10,
            pady=8
        )

        # ================================
        # 📦 TABLE CARD
        # ================================
        table_card = tk.Frame(
            container,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        table_card.pack(
            fill="both",
            expand=True
        )

        # ================================
        # HEADER TABLE
        # ================================
        table_header = tk.Frame(
            table_card,
            bg=PRIMARY_COLOR,
            height=40
        )

        table_header.pack(fill="x")
        table_header.pack_propagate(False)

        tk.Label(
            table_header,
            text="📋 Historique des actions",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 11, "bold")
        ).pack(
            side="left",
            padx=10,
            pady=8
        )

        # ================================
        # STYLE
        # ================================
        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=26,
            font=("Helvetica", 9),
            background=WHITE,
            fieldbackground=WHITE
        )

        style.configure(
            "Treeview.Heading",
            font=("Helvetica", 9, "bold")
        )

        # ================================
        # TABLE
        # ================================
        columns = (
            "Document",
            "Utilisateur",
            "Action",
            "Date",
            "Heure",
            "IP"
        )

        table = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings"
        )
        table.tag_configure(
            "download",
            foreground="#2980B9"
        )

        table.tag_configure(
            "edit",
            foreground="#F39C12"
        )

        table.tag_configure(
            "delete",
            foreground="#E74C3C"
        )

        table.tag_configure(
            "view",
            foreground="#27AE60"
        )
        
        activities = get_document_activities()

        for col in columns:
            table.heading(col, text=col)

        table.column("Document", width=220)
        table.column("Utilisateur", width=110, anchor="center")
        table.column("Action", width=120, anchor="center")
        table.column("Date", width=90, anchor="center")
        table.column("Heure", width=80, anchor="center")
        table.column("IP", width=150, anchor="center")
        
        # ================================
        # CHARGEMENT DES ACTIVITÉS
        # ================================
        def load_activities(data=None):

            table.delete(*table.get_children())

            if data is None:
                data = get_document_activities()

            for row in data:

                table.insert(
                    "",
                    "end",
                    values=row
                )

        # ================================
        # RECHERCHE LINÉAIRE
        # ================================
        def search_logs():

            keyword = search_entry.get().lower().strip()

            selected_action = action_filter.get()

            activities = get_document_activities()

            results = []

            for activity in activities:

                document = str(activity[0]).lower()
                user = str(activity[1]).lower()
                action = str(activity[2]).lower()
                date = str(activity[3]).lower()
                heure = str(activity[4]).lower()
                ip = str(activity[5]).lower()

                found = (
                    keyword in document or
                    keyword in user or
                    keyword in action or
                    keyword in date or
                    keyword in heure or
                    keyword in ip
                )

                if selected_action != "Toutes":

                    if found and action == selected_action.lower():
                        results.append(activity)

                else:

                    if found:
                        results.append(activity)

            load_activities(results)
            
        
        # ================================
        # ACTUALISER
        # ================================
        def refresh_logs():

            search_entry.delete(0, tk.END)

            action_filter.set("Toutes")

            load_activities()


        # ================================
        # BOUTONS
        # ================================
        tk.Button(
            filter_frame,
            text="🔎 Rechercher",
            bg=SUCCESS_COLOR,
            fg=WHITE,
            bd=0,
            padx=10,
            command=search_logs
        ).pack(
            side="right",
            padx=5,
            pady=8
        )

        # tk.Button(
        #     filter_frame,
        #     text="🔄 Actualiser",
        #     bg=SECONDARY_COLOR,
        #     fg=WHITE,
        #     bd=0,
        #     padx=10,
        #     command=refresh_logs
        # ).pack(
        #     side="right",
        #     padx=5,
        #     pady=8
        # )

        # Recherche en temps réel
        search_entry.bind(
            "<KeyRelease>",
            lambda e: search_logs()
        )
        
        
        activities = get_document_activities()
        
        for activity in activities:
            document_name = activity[0]
            utilisateur   = activity[1] or "Inconnu"
            action        = activity[2]
            date_action   = activity[3]
            heure_action  = activity[4]
            ip_address    = activity[5] or "-"
            
            # ================================
            # 📄 ICÔNE DOCUMENT (SAFE VERSION)
            # ================================
            # ================================
            # 📄 ICÔNE DOCUMENT
            # ================================
            doc_name = str(document_name).lower() if document_name else ""
            
            if doc_name.endswith(".pdf"):
                icon = "📄"

            elif doc_name.endswith(".docx"):
                icon = "📝"

            elif doc_name.endswith(".xlsx"):
                icon = "📊"

            elif doc_name.endswith((".png", ".jpg", ".jpeg")):
                icon = "🖼"

            else:
                icon = "📁"

            # ================================
            # 🎯 TAG ACTION
            # ================================
            if action == "Téléchargement":
                tag = "download"
            elif action == "Modification":
                tag = "edit"

            elif action == "Suppression":
                tag = "delete"

            elif action == "Consultation":
                tag = "view"

            else:
                tag = ""


            # ================================
            # 📊 INSERTION DANS LE TABLEAU
            # ================================
            table.insert(
                "",
                "end",
                values=(
                    f"{icon} {document_name}",  # nom original conservé
                    utilisateur,
                    action,
                    date_action,    
                    heure_action,
                    ip_address
                ),
                tags=(tag,)
            )
            
        scrollbar = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=table.yview
        )

        table.configure(
            yscrollcommand=scrollbar.set
        )   

        scrollbar.pack(
            side="right",
            fill="y"
        )

        table.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )
    
    # ================================
    # 📊 MINI CARD LOG
    # ================================
    def _log_card(
        self,
        parent,
        title,
        value,
        color
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            width=170,
            height=70,
            bd=1,
            relief="solid"
        )

        card.pack(
            side="left",
            padx=5
        )

        card.pack_propagate(False)

        tk.Frame(
            card,
            bg=color,
            height=4
        ).pack(fill="x")

        tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 8)
        ).pack(pady=(8, 0))

        tk.Label(
            card,
            text=value,
            bg=WHITE,
            fg=color,
            font=("Helvetica", 14, "bold")
        ).pack()
    
    
    # ================================
    # 📦 DOCUMENTS PHYSIQUES
    # ================================
    def show_physical_documents(self):

        self.clear_body()
        self.page_title.config(text="📁 Gestion des Documents Physiques")

        # ================================
        # 🌟 CONTAINER PRINCIPAL
        # ================================
        container = tk.Frame(self.body, bg=LIGHT_COLOR)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # ================================
        # 📌 HEADER
        # ================================
        header = tk.Frame(container, bg=LIGHT_COLOR)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📁 Gestion des Documents Physiques",
            bg=LIGHT_COLOR,
            fg=PRIMARY_COLOR,
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Suivi des sorties, retours et rappels des archives physiques",
            bg=LIGHT_COLOR,
            fg="gray",
            font=("Helvetica", 9)
        ).pack(anchor="w")

        # ================================
        # 📊 STATS CARDS
        # ================================
        stats_frame = tk.Frame(container, bg=LIGHT_COLOR)
        stats_frame.pack(fill="x", pady=10)
        
        total = count_physical_documents()
        out = count_physical_out()
        returned = count_physical_returned()
        late = count_physical_late()
        due_today = count_due_today()
        
        self._log_card(stats_frame, "📂 Total", total, SECONDARY_COLOR)
        self._log_card(stats_frame, "📤 Sortis", out, WARNING_COLOR)
        self._log_card(stats_frame, "📥 Retours", returned, SUCCESS_COLOR)
        self._log_card(stats_frame, "⏰ Retards", late, DANGER_COLOR)
        self._log_card(stats_frame, "🔔 Aujourd'hui", due_today, PRIMARY_COLOR)

        # self._log_card(stats_frame, "📂 Total", "125", SECONDARY_COLOR)
        # self._log_card(stats_frame, "📤 Sortis", "18", WARNING_COLOR)
        # self._log_card(stats_frame, "📥 Retours", "95", SUCCESS_COLOR)
        # self._log_card(stats_frame, "⏰ Retards", "12", DANGER_COLOR)
        # self._log_card(stats_frame, "🔔 Rappels", "7", PRIMARY_COLOR)

        # ================================
        # 🔍 ZONE DE RECHERCHE
        # ================================
        search_frame = tk.Frame(container, bg=WHITE, bd=1, relief="solid")
        search_frame.pack(fill="x", pady=10)

        tk.Entry(
            search_frame,
            font=("Helvetica", 10),
            bd=0
        ).pack(side="left", padx=10, pady=8, fill="x", expand=True)

        ttk.Combobox(
            search_frame,
            values=["Tous", "Sorti", "Retourné", "En retard"],
            state="readonly",
            width=15
        ).pack(side="left", padx=5)

        ttk.Combobox(
            search_frame,
            values=["Tous"],
            state="readonly",
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="🔄 Actualiser",
            bg=SECONDARY_COLOR,
            fg=WHITE,
            bd=0,
            padx=10
        ).pack(side="right", padx=10)

        # ================================
        # 🎛 ACTIONS
        # ================================
        actions = tk.Frame(container, bg=LIGHT_COLOR)
        actions.pack(fill="x", pady=10)

        tk.Button(actions,text="➕ Nouvelle sortie",bg=PRIMARY_COLOR,fg=WHITE,command=self.open_new_sortie_form).pack(side="left", padx=5)
        tk.Button(actions, text="📥 Retour document", bg=SUCCESS_COLOR, fg=WHITE).pack(side="left", padx=5)
        tk.Button(actions, text="🔔 Rappels", bg=WARNING_COLOR, fg=WHITE).pack(side="left", padx=5)
        tk.Button(actions, text="🖨 Export PDF", bg=SECONDARY_COLOR, fg=WHITE).pack(side="left", padx=5)
        tk.Button(actions, text="📊 Statistiques", bg=DARK_COLOR, fg=WHITE).pack(side="left", padx=5)

        # ================================
        # 📋 TABLE (FULL VIEW FIX)
        # ================================

        table_frame = tk.Frame(container, bg=WHITE)
        table_frame.pack(fill="both", expand=True)

        columns = (
            "N°", "Document", "Référence", "Utilisateur",
            "Date sortie", "Heure", "Retour prévu",
            "Heure retour", "Statut"
        )

        # ================================
        # 🧾 TREEVIEW
        # ================================
        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # ================================
        # 📏 LARGEUR DES COLONNES (OPTIMISÉ)
        # ================================
        widths = {
            "N°": 50,
            "Document": 200,
            "Référence": 120,
            "Utilisateur": 150,
            "Date sortie": 110,
            "Heure": 80,
            "Retour prévu": 120,
            "Heure retour": 120,
            "Statut": 100
        }

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=widths.get(col, 100), anchor="center")

        # ================================
        # 📌 DONNÉES EXEMPLE
        # ================================
        data = [
            (1, "Dossier RH 2025", "RH-2025-001", "Jean Dupont",
            "29/06/2026", "14:30", "30/06/2026", "15:00", "Sorti"),

            (2, "Contrat Client A", "CT-2026-015", "Paul",
            "28/06/2026", "09:15", "29/06/2026", "10:00", "En retard"),

            (3, "Facture 2024", "FC-2024-122", "Marie",
            "25/06/2026", "11:00", "25/06/2026", "16:00", "Retourné"),
        ]

        for row in data:
            table.insert("", "end", values=row)

        # ================================
        # 📜 SCROLLBARS (IMPORTANT)
        # ================================

        # Vertical scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scroll_y.set)

        # Horizontal scrollbar
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
        table.configure(xscrollcommand=scroll_x.set)

        # ================================
        # 📦 PACK LAYOUT
        # ================================
        table.pack(side="top", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
    
    # ================================
    # Cette section gère les actions principales du formulaire :
    # - Validation des données saisies
    # - Enregistrement de la nouvelle sortie de document
    # - Génération automatique d’un identifiant unique
    # - Ajout dynamique des données dans le tableau principal (Treeview)
    # - Affichage des messages de succès ou d’erreur
    # - Fermeture sécurisée du formulaire après enregistrement
    # ================================
    def open_new_sortie_form(self):

        form = tk.Toplevel(self.body)
        form.title("➕ Nouvelle sortie de document")
        form.geometry("650x520")
        form.minsize(600, 480)
        form.configure(bg=LIGHT_COLOR)
        form.transient(self.body)
        form.grab_set()

        # ================================
        # HEADER
        # ================================
        header = tk.Frame(form, bg=PRIMARY_COLOR)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📤 Nouvelle sortie de document physique",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w", padx=10, pady=10)

        # ================================
        # SCROLLABLE AREA
        # ================================
        canvas = tk.Canvas(form, bg=LIGHT_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(form, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=LIGHT_COLOR)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ================================
        # STYLE HELPERS
        # ================================
        def add_placeholder(entry, text):
            entry.insert(0, text)
            entry.config(fg="gray")

            def on_focus_in(e):
                if entry.get() == text:
                    entry.delete(0, "end")
                    entry.config(fg="black")

            def on_focus_out(e):
                if entry.get() == "":
                    entry.insert(0, text)
                    entry.config(fg="gray")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

        def hover(btn, color1, color2):
            btn.bind("<Enter>", lambda e: btn.config(bg=color2))
            btn.bind("<Leave>", lambda e: btn.config(bg=color1))

        def mark_error(entry, is_error):
            entry.config(highlightthickness=2 if is_error else 0,
                        highlightbackground="red" if is_error else LIGHT_COLOR)

        # ================================
        # SECTION 1 - EMPREUNTEUR
        # ================================
        sec1 = ttk.LabelFrame(scroll_frame, text="👤 Informations emprunteur")
        sec1.pack(fill="x", padx=15, pady=10)

        sec1.grid_columnconfigure(0, weight=1)
        sec1.grid_columnconfigure(1, weight=1)
        sec1.grid_columnconfigure(2, weight=1)

        tk.Label(sec1, text="Nom").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        tk.Label(sec1, text="Service").grid(row=0, column=1, sticky="w", padx=5, pady=2)
        tk.Label(sec1, text="Téléphone").grid(row=0, column=2, sticky="w", padx=5, pady=2)

        borrower_name = tk.Entry(sec1)
        borrower_service = tk.Entry(sec1)
        borrower_phone = tk.Entry(sec1)

        borrower_name.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        borrower_service.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        borrower_phone.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        add_placeholder(borrower_name, "Ex: Jean Dupont")
        add_placeholder(borrower_service, "Ex: RH")
        add_placeholder(borrower_phone, "Ex: 237XX XXX XXX")
        
        # ================================
        # VALIDATION TÉLÉPHONE (CORRIGÉ)
        # ================================
        def validate_phone(char, current):
            return (char.isdigit() or char == "") and len(current) <= 9

            vcmd = (form.register(validate_phone), "%S", "%P")
            borrower_phone.config(validate="key", validatecommand=vcmd)
        
        # TAB fluide
        borrower_name.focus()

        # ================================
        # SECTION 2
        # ================================
        sec2 = ttk.LabelFrame(scroll_frame, text="📄 Document")
        sec2.pack(fill="x", padx=15, pady=10)

        sec2.grid_columnconfigure(0, weight=1)
        sec2.grid_columnconfigure(1, weight=1)

        tk.Label(sec2, text="Nom document").grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(sec2, text="Référence").grid(row=0, column=1, sticky="w", padx=5)

        document_name = tk.Entry(sec2)
        document_reference = tk.Entry(sec2)

        document_name.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        document_reference.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        add_placeholder(document_name, "Ex: Dossier RH 2025")
        add_placeholder(document_reference, "Ex: RH-2025-001")

        # ================================
        # SECTION 3
        # ================================
        sec3 = ttk.LabelFrame(scroll_frame, text="⏰ Retour & Motif")
        sec3.pack(fill="x", padx=15, pady=10)

        sec3.grid_columnconfigure(0, weight=1)
        sec3.grid_columnconfigure(1, weight=1)

        tk.Label(sec3, text="Motif").grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(sec3, text="Date retour").grid(row=0, column=1, sticky="w", padx=5)

        reason = tk.Entry(sec3)
        expected_return = tk.Entry(sec3)

        reason.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        expected_return.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        add_placeholder(reason, "Ex: Consultation")
        add_placeholder(expected_return, "YYYY-MM-DD")

        tk.Label(sec3, text="Heure retour").grid(row=2, column=0, sticky="w", padx=5)

        expected_return_time = tk.Entry(sec3)
        expected_return_time.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        add_placeholder(expected_return_time, "HH:MM")

        # ================================
        # SECTION 4
        # ================================
        sec4 = ttk.LabelFrame(scroll_frame, text="📝 Notes")
        sec4.pack(fill="x", padx=15, pady=10)

        notes = tk.Entry(sec4)
        notes.pack(fill="x", padx=5, pady=5)

        add_placeholder(notes, "Notes supplémentaires...")

        # ================================
        # ACTIONS
        # ================================
        actions = tk.Frame(form, bg=LIGHT_COLOR)
        actions.pack(fill="x", pady=10)

        def save():

            fields = [
                borrower_name,
                borrower_phone,   # ✅ ajouté
                document_name,
                expected_return,
                expected_return_time
            ]

            valid = True

            for f in fields:
                is_empty = f.get() == "" or f.get().startswith("Ex:")
                mark_error(f, is_empty)
                if is_empty:
                    valid = False

            if not valid:
                tk.messagebox.showerror("Erreur", "Champs obligatoires manquants")
                return

            try:
                import sqlite3

                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO physical_document_loans (
                        borrower_name,
                        borrower_service,
                        borrower_phone,
                        document_name,
                        document_reference,
                        reason,
                        expected_return,
                        expected_return_time,
                        notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                        borrower_name.get(),
                        borrower_service.get(),
                        borrower_phone.get(),
                        document_name.get(),
                        document_reference.get(),
                        reason.get(),
                        expected_return.get(),
                        expected_return_time.get(),
                        notes.get()
                    ))

                conn.commit()
                conn.close()

                tk.messagebox.showinfo("Succès", "Sortie enregistrée")
                form.destroy()

                if hasattr(self, "refresh_physical_table"):
                    self.refresh_physical_table()

            except Exception as e:
                tk.messagebox.showerror("Erreur DB", str(e))

        btn_save = tk.Button(
            actions,
            text="💾 Enregistrer",
            bg=SUCCESS_COLOR,
            fg=WHITE,
            command=save
        )
        btn_save.pack(side="right", padx=10)

        btn_close = tk.Button(
            actions,
            text="❌ Fermer",
            bg=DANGER_COLOR,
            fg=WHITE,
            command=form.destroy
        )
        btn_close.pack(side="right")

        # HOVER ANIMATION
        hover(btn_save, SUCCESS_COLOR, "#27AE60")
        hover(btn_close, DANGER_COLOR, "#C0392B")