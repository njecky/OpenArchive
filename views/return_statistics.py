# ================================
# 📊 RETURN STATISTICS VIEW
# ================================

import tkinter as tk

from config.constants import *

from controllers.statistics_controller import get_statistics



class ReturnStatistics:


    def __init__(self, root):

        self.window = tk.Toplevel(root)

        self.window.title(
            "📊 Statistiques des retours"
        )

        self.window.geometry(
            "900x600"
        )

        self.window.configure(
            bg=LIGHT_COLOR
        )


        self.build_ui()



    # ================================
    # 🎨 INTERFACE
    # ================================
    def build_ui(self):


        title = tk.Label(
            self.window,

            text="📊 TABLEAU DE BORD - RETOURS DOCUMENTS",

            font=(
                "Arial",
                18,
                "bold"
            ),

            bg=LIGHT_COLOR,

            fg=PRIMARY_COLOR
        )


        title.pack(
            pady=20
        )


        self.stats = get_statistics()



        cards = tk.Frame(
            self.window,

            bg=LIGHT_COLOR
        )


        cards.pack(
            fill="x",
            padx=20
        )



        self.create_card(
            cards,
            "📄 Documents empruntés",
            self.stats["total_loans"]
        )


        self.create_card(
            cards,
            "✅ Documents retournés",
            self.stats["returned"]
        )


        self.create_card(
            cards,
            "🚨 Documents en retard",
            self.stats["overdue"]
        )


        self.create_card(
            cards,
            "📅 Aujourd'hui",
            self.stats["today"]
        )


        self.create_card(
            cards,
            "⏳ À venir",
            self.stats["upcoming"]
        )


        self.create_card(
            cards,
            "📈 Taux retour",
            f"{self.stats['rate']} %"
        )


        self.create_chart()



    # ================================
    # 🃏 CARTE KPI
    # ================================
    def create_card(
            self,
            parent,
            title,
            value
    ):


        card = tk.Frame(
            parent,

            bg=WHITE,

            width=220,

            height=90,

            relief="ridge",

            bd=1
        )


        card.pack(
            side="left",

            padx=8,

            pady=10
        )


        card.pack_propagate(False)



        tk.Label(
            card,

            text=title,

            font=(
                "Arial",
                10,
                "bold"
            ),

            bg=WHITE,

            fg=PRIMARY_COLOR
        ).pack(
            pady=5
        )


        tk.Label(
            card,

            text=value,

            font=(
                "Arial",
                20,
                "bold"
            ),

            bg=WHITE,

            fg=SECONDARY_COLOR
        ).pack()



    # ================================
    # 📊 GRAPHIQUE BARRES
    # ================================
    def create_chart(self):


        frame = tk.Frame(
            self.window,

            bg=LIGHT_COLOR
        )


        frame.pack(
            pady=30
        )


        data = {

            "Retournés":
                self.stats["returned"],

            "Retard":
                self.stats["overdue"],

            "Aujourd'hui":
                self.stats["today"],

            "À venir":
                self.stats["upcoming"]

        }



        tk.Label(
            frame,

            text="📊 Répartition",

            font=(
                "Arial",
                14,
                "bold"
            ),

            bg=LIGHT_COLOR
        ).pack()



        for label,value in data.items():


            row = tk.Frame(
                frame,

                bg=LIGHT_COLOR
            )

            row.pack(
                pady=5
            )



            tk.Label(
                row,

                text=label,

                width=15,

                anchor="w",

                bg=LIGHT_COLOR
            ).pack(
                side="left"
            )



            bar = "█" * value


            tk.Label(
                row,

                text=bar,

                fg=SUCCESS_COLOR,

                bg=LIGHT_COLOR
            ).pack(
                side="left"
            )


            tk.Label(
                row,

                text=f" {value}",

                bg=LIGHT_COLOR
            ).pack(
                side="left"
            )