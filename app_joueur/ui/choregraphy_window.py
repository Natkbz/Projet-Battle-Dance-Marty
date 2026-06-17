from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton,QFileDialog
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer
import random

class EyesWidget(QWidget):
    
    def __init__(self, color="#6395EE"):
        super().__init__()
        self.setFixedSize(220, 100)
        self.eye_color = color

    def set_color(self, color: str):
        self.eye_color = color
        self.update()  # force le redessin

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._draw_eye(painter, 20, 10)
        self._draw_eye(painter, 120, 10)

    def _draw_eye(self, painter, x, y):
        size = 80
        painter.setBrush(QColor("#e8f0ff"))
        painter.setPen(QColor(self.eye_color))
        painter.drawEllipse(x, y, size, size)
        pupil_size = 48
        px = x + (size - pupil_size) // 2
        py = y + (size - pupil_size) // 2
        painter.setBrush(QColor(self.eye_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(px, py, pupil_size, pupil_size)
        painter.setBrush(QColor(255, 255, 255, 140))
        painter.drawEllipse(x + 52, y + 14, 16, 16)

class DanceThread(QThread):
    """Thread qui gère la danse pour ne pas bloquer l'UI."""
    # Signal émis quand la danse est finie, il transporte le score (un entier)
    finished_dance = pyqtSignal(int)

    def __init__(self, marty_dance):
        super().__init__()
        self.marty_dance = marty_dance

    def run(self):
        # Cette méthode s'exécute en arrière-plan
        try:
            score = self.marty_dance.dance()
            # On vérifie qu'on a bien un score valide avant de l'émettre
            score_val = int(score) if score is not None else 0
            self.finished_dance.emit(score_val)
        except Exception as e:
            print(f"Erreur pendant la danse : {e}")
            self.finished_dance.emit(0)

class ChoregraphyWindow(QMainWindow):

    def __init__(self, file_path: str, marty, marty_dance_, parent=None):
        super().__init__()
        self.file_path = file_path
        self.marty = marty
        self.marty_dance = marty_dance_
        print(self.marty_dance, marty_dance_)
        self.parent_window = parent
        self.is_running = False
        
        self.eye_timer = QTimer(self)
        self.eye_timer.timeout.connect(self.animate_eyes)
        self.party_colors = ["#6395EE", "#EE6363", "#62C6AA", "#EE63D2", "#EEEE63", "#9563EE", "#FF8C00"]
        self.dance_thread = None

        self.setWindowTitle("Chorégraphie en cours")
        self.setMinimumSize(500, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        central_widget.setLayout(layout)

        # Yeux de Marty
        self.eyes = EyesWidget(color="#6395EE")
        layout.addWidget(self.eyes, alignment=Qt.AlignmentFlag.AlignCenter)

        # Statut
        self.status_label = QLabel("Prêt à lancer")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("heading")
        layout.addWidget(self.status_label)

        # Nom du fichier
        file_name = file_path.split("/")[-1]
        self.file_label = QLabel(f"{file_name}") 
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setObjectName("subheading")
        layout.addWidget(self.file_label)

        # Bouton lancer
        self.btn_start = QPushButton("▶  Lancer")
        self.btn_start.setObjectName("btn_primary")
        self.btn_start.clicked.connect(self.on_start)
        layout.addWidget(self.btn_start)
        
        #bouton pour charger un nouveau fichier
        self.btn_load_new = QPushButton("📁 Charger un autre fichier")
        self.btn_load_new.setObjectName("btn_secondary") # ou btn_primary selon ton QSS
        self.btn_load_new.clicked.connect(self.on_load_new)
        layout.addWidget(self.btn_load_new)

    def on_start(self):
        self.is_running = True
        self.status_label.setText("Chorégraphie en cours...")
        self.btn_start.setVisible(False)
        self.btn_load_new.setVisible(False)
        
        # Lance le clignotement des yeux toutes les 400 ms
        self.eye_timer.start(400)
        
        # Prépare et lance le thread de danse en arrière-plan
        self.dance_thread = DanceThread(self.marty_dance)
        self.dance_thread.finished_dance.connect(self.on_dance_finished)
        self.dance_thread.start()
    
    def animate_eyes(self):
        """Choisit une couleur au hasard pour animer les yeux."""
        color = random.choice(self.party_colors)
        self.eyes.set_color(color)

    def on_dance_finished(self, score):
        """Appelée automatiquement quand Marty a fini sa danse."""
        self.is_running = False
        
        # Arrête le changement de couleur automatique
        self.eye_timer.stop()
        
        # Remet l'UI à jour avec le score
        self.status_label.setText(f"Score : {score}")
        self.eyes.set_color("#88CFA8")  # Vert = terminé
        self.btn_start.setVisible(True)
        self.btn_start.setText("▶  Relancer")
        self.btn_load_new.setVisible(True)
    def on_load_new(self):
        """Ouvre un explorateur pour charger un nouveau fichier .dance."""
        # On ouvre la fenêtre Windows/Mac pour choisir le fichier
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choisir une autre chorégraphie", "",
            "Fichiers Dance (*.dance);;Tous les fichiers (*)"
        )
        
        # Si l'utilisateur a bien choisi un fichie
        if file_path:
            self.file_path = file_path
            file_name = file_path.split("/")[-1]
            self.file_label.setText(file_name) # On change le nom écrit sur l'interface
            
            try:
                # Le robot charge les nouvelles données.
                self.marty_dance.new_dance(file_path)
                
                # On rafraîchit l'interface pour qu'elle soit prête pour un nouveau clic
                self.status_label.setText("Nouvelle chorégraphie chargée !")
                self.eyes.set_color("#6395EE")  # Les yeux redeviennent bleus (prêt)
                self.btn_start.setText("▶  Lancer")
                
            except Exception as e:
                self.status_label.setText("Erreur lors du décodage du fichier")
                print(f"Erreur de chargement : {e}")
    
    def _return_to_control(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

    def closeEvent(self, event):  
        # Si le thread tourne encore, on l'arrête 
        if self.is_running and self.dance_thread:
            self.dance_thread.terminate() 
            
        if self.parent_window:
            self.parent_window.show()
        self.marty_dance.end_battle()
        event.accept()