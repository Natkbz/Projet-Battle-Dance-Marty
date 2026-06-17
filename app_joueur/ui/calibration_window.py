from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QComboBox
)
from PyQt6.QtCore import Qt

class CalibrationWindow(QMainWindow):

    def __init__(self, marty, parent=None):
        super().__init__()
        self.marty = marty
        self.parent_window = parent

        self.setWindowTitle("Calibration des couleurs")
        self.setMinimumSize(400, 300)
        
        # widget central + layout vertical centré avec des marges
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(28, 28, 28, 28)
        central_widget.setLayout(layout)
        
        heading = QLabel("Calibration des couleurs")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setObjectName("heading")
        layout.addWidget(heading)
        
        self.color_select = QComboBox() # crée le menu déroulant
        self.colors = { # dictionnaire clé (code : utilisé par Marty) -> valeur (name : nom affiché)
            "N": "Noir", "Y": "Jaune", "G": "Vert",
            "R": "Rouge", "P": "Mauve", "C": "Bleu ciel", "B": "Bleu foncé"
        }
        
        for code, name in self.colors.items():
            # addItem peut prendre 2 params, le 2ème permet d'associer des données à l'élément ajouté (name)
            self.color_select.addItem(name, code) # ajoute les couleurs au menu déroulant
            
        layout.addWidget(self.color_select)
        
        self.instructions_label = QLabel("Placez le robot sur la couleur choisie, puis cliquez sur Calibrer.")
        self.instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_label.setObjectName("subheading")
        self.instructions_label.setWordWrap(True) # revient à la ligne si texte trop long par rapport à la largeur de la fenêtre (évite le dépassemnt)
        layout.addWidget(self.instructions_label)
        
        self.btn_calibrate = QPushButton("Calibrer cette couleur")
        self.btn_calibrate.setObjectName("btn_primary")
        self.btn_calibrate.clicked.connect(self.calibrate)
        layout.addWidget(self.btn_calibrate)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("status")
        layout.addWidget(self.status_label)
    
    def calibrate(self):
        code = self.color_select.currentData() # repère la donnée cachée (code) de l'option actuellement séléctionnée 
        color_name = self.colors[code]

        self._set_status(f"Calibration de {color_name} en cours...", "status")

        values = self.marty.martyColor.captureColorValue(code)

        self._set_status(f"{color_name} calibré : {values}", "status_ok")
        
    def _set_status(self, message: str, style_name: str):
        self.status_label.setText(message)
        self.status_label.setObjectName(style_name)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        
    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
        
        