# ================================
# 🚀 MAIN - ArchivaDesk
# ================================

import tkinter as tk

from config.constants import *
from views.splash import SplashScreen
from models.model import init_db
# IMPORT DB
# from models.model import init_db

# ================================
# 🔹 MAIN
# ================================
def main():

    # INITIALISER SQLITE
    init_db()

    # Fenêtre principale
    root = tk.Tk()

    root.attributes('-alpha', 0)

    root.title(APP_NAME)
    root.resizable(False, False)

    root.withdraw()

    # Splash
    SplashScreen(root)

    root.mainloop()

# ================================
# ▶️ START
# ================================
if __name__ == "__main__":
    main()