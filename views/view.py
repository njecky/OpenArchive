import customtkinter as ctk
from tkinter import ttk, Menu
from config.constants import APP_NAME, COLOR_PRIMARY, COLOR_BG
import config.function as fn  # Import des fonctions
from controllers.controller import ContactController

class ContactView(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.master.title(APP_NAME)

        # Taille fixe + centrage
        w, h = 800, 500
        x = (self.master.winfo_screenwidth() // 2) - (w // 2)
        y = (self.master.winfo_screenheight() // 2) - (h // 2)
        self.master.geometry(f"{w}x{h}+{x}+{y}")

        self.master.configure(fg_color=COLOR_BG)
        self.master.resizable(False, False)

        # === MENU ===
        menubar = Menu(self.master)

        # --- Menu Fichier ---
        file_menu = Menu(menubar, tearoff=0)
        # file_menu.add_command(label="Nouveau contact", command=fn.new_contact, accelerator="Ctrl+N")
        file_menu.add_command(label="Nouveau contact",command=lambda: fn.new_contact(self.controller), accelerator="Ctrl+N")
        file_menu.add_command(label="Importer", command=fn.import_contacts, accelerator="Ctrl+I")
        file_menu.add_command(label="Exporter", command=fn.export_contacts, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=lambda: fn.quit_app(self.master), accelerator="Ctrl+Q")
        menubar.add_cascade(label="Fichier", menu=file_menu)

        # --- Menu Contacts ---
        contact_menu = Menu(menubar, tearoff=0)
        contact_menu.add_command(label="Ajouter", command=fn.add_contact, accelerator="Ctrl+A")
        contact_menu.add_command(label="Modifier", command=fn.edit_contact, accelerator="Ctrl+M")
        contact_menu.add_command(label="Supprimer", command=fn.delete_contact, accelerator="Ctrl+D")
        contact_menu.add_command(label="Rechercher", command=lambda: fn.focus_search(self.search_entry), accelerator="Ctrl+R")
        menubar.add_cascade(label="Contacts", menu=contact_menu)

        # --- Menu Aide ---
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="À propos", command=fn.about, accelerator="F1")
        help_menu.add_command(label="Mise à jour", command=fn.update_app, accelerator="F2")
        help_menu.add_command(label="Guide d'utilisation", command=fn.user_guide, accelerator="F3")
        menubar.add_cascade(label="Aide", menu=help_menu)

        self.master.config(menu=menubar)

        # === Barre de recherche ===
        search_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        search_frame.pack(fill="x", pady=10, padx=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Rechercher un contact...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Quand on tape une touche -> recherche séquentielle
        self.search_entry.bind("<KeyRelease>",lambda e: self.controller.search_contacts(self.search_entry.get().strip()))
        
        self.search_button = ctk.CTkButton(search_frame,text="Rechercher",fg_color=COLOR_PRIMARY,command=lambda: self.controller.search_contacts(self.search_entry.get().strip()))
        # self.search_button = ctk.CTkButton(search_frame, text="Rechercher", fg_color=COLOR_PRIMARY)
        self.search_button.pack(side="left", padx=5)
        # Quand l’utilisateur appuie sur ENTRÉE dans le champ recherche
        self.search_entry.bind("<Return>",lambda e: self.controller.search_contacts(self.search_entry.get().strip()))
        # === Tableau des contacts ===
        # table_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        # table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # self.tree = ttk.Treeview(table_frame, columns=("Nom", "Téléphone", "Email", "Catégorie"), show="headings")
        # self.tree.heading("Nom", text="Nom")
        # self.tree.heading("Téléphone", text="Téléphone")
        # self.tree.heading("Email", text="Email")
        # self.tree.heading("Catégorie", text="Catégorie")
        # self.tree.pack(fill="both", expand=True)
        # === Tableau des contacts ===
        table_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Nom", "Téléphone", "Email", "Catégorie"),
            show="headings"
        )
        
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Téléphone", text="Téléphone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Catégorie", text="Catégorie")
        self.tree.pack(fill="both", expand=True)

        # === Maintenant que le tableau existe, on peut créer le contrôleur ===
        from controllers.controller import ContactController
        self.controller = ContactController(self)

        # === Boutons d'action ===
        action_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        action_frame.pack(fill="x", pady=10)

        self.add_button = ctk.CTkButton(action_frame, text="Ajouter", fg_color=COLOR_PRIMARY, command=fn.add_contact)
        self.add_button.pack(side="left", padx=5)

        self.edit_button = ctk.CTkButton(action_frame, text="Modifier", fg_color=COLOR_PRIMARY, command=fn.edit_contact)
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ctk.CTkButton(action_frame, text="Supprimer", fg_color="red", command=fn.delete_contact)
        self.delete_button.pack(side="left", padx=5)

        self.pack(fill="both", expand=True)

        # === Raccourcis clavier globaux ===
        self.master.bind("<Control-n>", lambda e: fn.new_contact())
        self.master.bind("<Control-i>", lambda e: fn.import_contacts())
        self.master.bind("<Control-e>", lambda e: fn.export_contacts())
        self.master.bind("<Control-q>", lambda e: fn.quit_app(self.master))

        self.master.bind("<Control-a>", lambda e: fn.add_contact())
        self.master.bind("<Control-m>", lambda e: fn.edit_contact())
        self.master.bind("<Control-d>", lambda e: fn.delete_contact())
        self.master.bind("<Control-r>", lambda e: fn.focus_search(self.search_entry))

        self.master.bind("<F1>", lambda e: fn.about())
        self.master.bind("<F2>", lambda e: fn.update_app())
        self.master.bind("<F3>", lambda e: fn.user_guide())
