# ================================
# 📦 RETURN DOCUMENTS VIEW
# ================================
import tkinter as tk
from tkinter import ttk, messagebox
from config.constants import *
from controllers.return_controller import *
from config.function import *


class ReturnDocumentsWindow:

    def __init__(self, root):

        self.root = tk.Toplevel(root)
        self.root.title("📥 Retour documents")
        self.root.geometry(f"{WINDOW_WIDTH-200}x{WINDOW_HEIGHT-100}")
        self.root.configure(bg=LIGHT_COLOR)

        self.selected_id = None

        self.build_ui()
        self.load_data()

    # ================================
    # 🎨 INTERFACE
    # ================================
    def build_ui(self):

        header = tk.Label(
            self.root,
            text="📥 Gestion des retours documents",
            font=("Arial", 16, "bold"),
            bg=LIGHT_COLOR,
            fg=PRIMARY_COLOR
        )
        header.pack(pady=10)

        # ================================
        # TABLE
        # ================================
        columns = ("ID", "Document", "Emprunteur", "Téléphone", "Retour prévu", "Statut")

        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ================================
        # ACTIONS
        # ================================
        actions = tk.Frame(self.root, bg=LIGHT_COLOR)
        actions.pack(pady=10)

        btn = tk.Button(
            actions,
            text="📥 Marquer retourné",
            bg=SUCCESS_COLOR,
            fg=WHITE,
            command=self.return_document
        )
        btn.pack(side="left", padx=5)

        tk.Button(
            actions,
            text="🔄 Rafraîchir",
            bg=SECONDARY_COLOR,
            fg=WHITE,
            command=self.load_data
        ).pack(side="left", padx=5)

    # ================================
    # 📊 CHARGER DONNÉES
    # ================================
    def load_data(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        data = get_pending_returns()

        for row in data:
            self.tree.insert("", "end", values=row)

    # ================================
    # 🎯 SÉLECTION
    # ================================
    def on_select(self, event):

        selected = self.tree.selection()

        if selected:
            values = self.tree.item(selected[0])["values"]
            self.selected_id = values[0]

    # ================================
    # 📥 RETOUR DOCUMENT
    # ================================
    def return_document(self):

        if not self.selected_id:
            messagebox.showwarning(
                "Retour",
                "Veuillez sélectionner un document."
            )
            return

        try:

            mark_document_returned(self.selected_id)
            add_return_log(self.selected_id)

            messagebox.showinfo(
                "Succès",
                "Document marqué comme retourné avec succès."
            )

            self.load_data()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))