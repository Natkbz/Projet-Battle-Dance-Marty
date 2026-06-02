import sys
from PyQt6.QtWidgets import QApplication
from ui.connection_window import ConnectionWindow

app = QApplication(sys.argv)

with open("app_joueur/styles/robot-connection.qss", "r") as f:
    app.setStyleSheet(f.read())

window = ConnectionWindow()
window.show()

sys.exit(app.exec())