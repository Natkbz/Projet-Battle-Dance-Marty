import sys
from PyQt6.QtWidgets import QApplication
from UI.fileWindow import FileWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # CHARGEMENT DU FICHIER QSS
    try:
        with open("app_server/styles/server.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        print("Fichier style.qss introuvable")
    #lancement de la première fenetre ou on doit choisir un fichier .battle
    fenetre_demarrage = FileWindow()
    fenetre_demarrage.show()
    
    sys.exit(app.exec())