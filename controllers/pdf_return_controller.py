# ================================
# 📄 GÉNÉRATION PDF
# ================================
import sqlite3
from datetime import datetime
from tkinter import filedialog

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from config.constants import *


# ================================
# 📄 EXPORTER LE RAPPORT PDF
# ================================
def export_return_report():

    # ================================
    # 📁 CHOIX DU FICHIER PDF
    # ================================
    filename = filedialog.asksaveasfilename(

        title="Enregistrer le rapport PDF",

        defaultextension=".pdf",

        initialfile=f"Rapport_Retours_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",

        filetypes=[

            ("Fichier PDF", "*.pdf")

        ]

    )

    if not filename:

        return

    # ================================
    # 🗄 CONNEXION SQLITE
    # ================================
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            document_name,

            borrower_name,

            borrower_phone,

            expected_return,

            expected_return_time,

            status

        FROM physical_document_loans

        ORDER BY

            expected_return ASC,

            expected_return_time ASC

    """)

    documents = cursor.fetchall()

    conn.close()

    # ================================
    # 📄 CRÉATION DU PDF
    # ================================
    pdf = SimpleDocTemplate(

        filename,

        pagesize=A4

    )

    styles = getSampleStyleSheet()

    elements = []

    # ================================
    # 🏢 TITRE
    # ================================
    elements.append(

        Paragraph(

            "<font size='20'><b>DigiBox</b></font>",

            styles["Title"]

        )

    )

    elements.append(

        Paragraph(

            "<b>Rapport des retours de documents</b>",

            styles["Heading2"]

        )

    )

    elements.append(

        Paragraph(

            f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",

            styles["Normal"]

        )

    )

    elements.append(

        Spacer(

            1,

            20

        )

    )

    # ================================
    # 📋 TABLE
    # ================================
    data = [

        [

            "Document",

            "Emprunteur",

            "Téléphone",

            "Date retour",

            "Heure",

            "Statut"

        ]

    ]

    # ================================
    # 📄 DONNÉES
    # ================================
    for document in documents:

        data.append(

            [

                document[0],

                document[1],

                document[2],

                document[3],

                document[4],

                document[5]

            ]

        )

    table = Table(data)

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("FONTSIZE", (0, 0), (-1, 0), 10),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige)

            ]

        )

    )

    elements.append(

        table

    )

    elements.append(

        Spacer(

            1,

            25

        )

    )

    # ================================
    # 📊 STATISTIQUES
    # ================================
    total = len(documents)

    returned = sum(1 for d in documents if d[5] == "Returned")

    outgoing = sum(1 for d in documents if d[5] == "Sorti")

    elements.append(

        Paragraph(

            f"<b>Total des documents :</b> {total}",

            styles["Normal"]

        )

    )

    elements.append(

        Paragraph(

            f"<b>Documents retournés :</b> {returned}",

            styles["Normal"]

        )

    )

    elements.append(

        Paragraph(

            f"<b>Documents sortis :</b> {outgoing}",

            styles["Normal"]

        )

    )

    elements.append(

        Spacer(

            1,

            30

        )

    )

    # ================================
    # ✍ SIGNATURE
    # ================================
    elements.append(

        Paragraph(

            "Archiviste ______________________________",

            styles["Normal"]

        )

    )

    # ================================
    # 💾 GÉNÉRATION PDF
    # ================================
    pdf.build(

        elements

    )

    return filename