# controllers/controller.py
import tkinter as tk
from tkinter import messagebox
from models import model

class ContactController:
    def __init__(self, view):
        self.view = view
        # Initialiser la base si pas encore créée
        model.init_db()
        # Charger les contacts dès l’ouverture
        self.load_contacts()

    def load_contacts(self):
        """Charge tous les contacts depuis la BDD et les affiche dans le tableau"""
        self.view.tree.delete(*self.view.tree.get_children())  # vider le tableau
        contacts = model.get_contacts()
        for contact in contacts:
            contact_id, nom, tel, email, categorie = contact
            self.view.tree.insert("", "end", iid=contact_id, values=(nom, tel, email, categorie))

    def add_contact(self, nom, tel, email, categorie):
        """Ajoute un contact et rafraîchit la vue"""
        model.add_contact(nom, tel, email, categorie)
        self.load_contacts()

    def delete_contact(self, contact_id):
        """Supprime un contact et rafraîchit"""
        model.delete_contact(contact_id)
        self.load_contacts()
    
    def search_contacts(self, keyword):
        """Recherche et affiche seulement les résultats"""
        self.view.tree.delete(*self.view.tree.get_children())

        if not keyword:  # champ vide => afficher un message
            messagebox.showwarning("Champ vide", "Veuillez entrer un mot-clé pour la recherche.")
            return

        results = model.search_contacts(keyword)
        for contact in results:
            contact_id, nom, tel, email, categorie = contact
            self.view.tree.insert("", "end", iid=contact_id, values=(nom, tel, email, categorie))
    # def search_contacts(self, keyword):
    #     """Recherche et affiche seulement les résultats"""
    #     self.view.tree.delete(*self.view.tree.get_children())
    #     results = model.search_contacts(keyword)
    #     for contact in results:
    #         contact_id, nom, tel, email, categorie = contact
    #         self.view.tree.insert("", "end", iid=contact_id, values=(nom, tel, email, categorie))
