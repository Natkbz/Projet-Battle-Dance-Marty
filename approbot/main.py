import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QFont

# classe MainWindow qui hérite de QMainWindow 
# et qui permet de personnaliser les fenêtres 
# qu'on affichent à l'utiilsateur 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NDDance")
        self.setMinimumSize(800,600)
        self.setWindowIcon(QIcon("approbot/assets/images/robot_icon.png")) # icône de la fenêtre (à définir)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        label = QLabel("Contrôle du robot", self)
        label.setFont(QFont("approbot/assets/fonts/Roboto-Regular.ttf", 30))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label)
        
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)
        
        btn_left = QPushButton("Gauche")
        btn_right = QPushButton("Droite")
        btn_top = QPushButton("Haut")
        btn_bottom = QPushButton("Bas")
        
        buttons_layout.addWidget(btn_left)
        buttons_layout.addWidget(btn_right)
        buttons_layout.addWidget(btn_top)
        buttons_layout.addWidget(btn_bottom)
        
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())