from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QGridLayout, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon
from robot.MartyContext import MartyContext

class ControlWindow(QMainWindow):
    def __init__(self, marty):
        super().__init__()
        self.marty = marty
        self.setWindowTitle("Controle")
        self.setMinimumSize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Batterie en haut à droite
        self.battery_label = QLabel("Batterie : Inconnue")
        self.battery_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.battery_label.setObjectName("battery_label")
        main_layout.addWidget(self.battery_label)

        # Zone principale (bras | flèches+couleur)
        main_area = QHBoxLayout()
        main_layout.addLayout(main_area)

        # Colonne bras (à gauche) 
        arms_layout = QVBoxLayout()
        arms_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        arms_layout.setSpacing(10)

        icon_size = QSize(50, 50)
        btn_size = 70  # taille carrée des boutons bras

        self.btn_arm_right_back = QPushButton()
        self.btn_arm_right_back.setIcon(QIcon("app_joueur/assets/images/bras_arriere.png"))
        self.btn_arm_right_back.setIconSize(icon_size)
        self.btn_arm_right_back.setFixedSize(btn_size, btn_size)
        self.btn_arm_right_back.setToolTip("Bras droit arrière")
        self.btn_arm_right_back.setObjectName("btn_arm")
        self.btn_arm_right_back.clicked.connect(self.on_arm_right_back)
        arms_layout.addWidget(self.btn_arm_right_back)

        self.btn_arm_left_back = QPushButton()
        self.btn_arm_left_back.setIcon(QIcon("app_joueur/assets/images/bras_arriere.png"))
        self.btn_arm_left_back.setIconSize(icon_size)
        self.btn_arm_left_back.setFixedSize(btn_size, btn_size)
        self.btn_arm_left_back.setToolTip("Bras gauche arrière")
        self.btn_arm_left_back.setObjectName("btn_arm")
        self.btn_arm_left_back.clicked.connect(self.on_arm_left_back)
        arms_layout.addWidget(self.btn_arm_left_back)

        self.btn_arm_right_up = QPushButton()
        self.btn_arm_right_up.setIcon(QIcon("app_joueur/assets/images/lever_bras_droit.png"))
        self.btn_arm_right_up.setIconSize(icon_size)
        self.btn_arm_right_up.setFixedSize(btn_size, btn_size)
        self.btn_arm_right_up.setToolTip("Lever bras droit")
        self.btn_arm_right_up.setObjectName("btn_arm")
        self.btn_arm_right_up.clicked.connect(self.on_arm_right_up)
        arms_layout.addWidget(self.btn_arm_right_up)

        self.btn_arm_left_up = QPushButton()
        self.btn_arm_left_up.setIcon(QIcon("app_joueur/assets/images/lever_bras_gauche.png"))
        self.btn_arm_left_up.setIconSize(icon_size)
        self.btn_arm_left_up.setFixedSize(btn_size, btn_size)
        self.btn_arm_left_up.setToolTip("Lever bras gauche")
        self.btn_arm_left_up.setObjectName("btn_arm")
        self.btn_arm_left_up.clicked.connect(self.on_arm_left_up)
        arms_layout.addWidget(self.btn_arm_left_up)

        main_area.addLayout(arms_layout)

        # Zone centrale : flèches + couleur 
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Grille des flèches avec bouton stand_straight au centre
        grid = QGridLayout()
        grid.setSpacing(10)

        self.btn_forward = QPushButton("↑")
        self.btn_forward.setObjectName("btn_forward")
        self.btn_forward.clicked.connect(self.on_forward)
        grid.addWidget(self.btn_forward, 0, 1)

        self.btn_left = QPushButton("←")
        self.btn_left.setObjectName("btn_left")
        self.btn_left.clicked.connect(self.on_left)
        grid.addWidget(self.btn_left, 1, 0)

        # Bouton stand_straight au centre
        self.btn_stand = QPushButton("⬛")
        self.btn_stand.setObjectName("btn_stand")
        self.btn_stand.setToolTip("Se redresser")
        self.btn_stand.clicked.connect(self.on_stand)
        grid.addWidget(self.btn_stand, 1, 1)

        self.btn_right = QPushButton("→")
        self.btn_right.setObjectName("btn_right")
        self.btn_right.clicked.connect(self.on_right)
        grid.addWidget(self.btn_right, 1, 2)

        self.btn_backward = QPushButton("↓")
        self.btn_backward.setObjectName("btn_backward")
        self.btn_backward.clicked.connect(self.on_backward)
        grid.addWidget(self.btn_backward, 2, 1)

        center_layout.addLayout(grid)

        # Carré couleur sous les flèches
        self.color_label = QLabel()
        self.color_label.setFixedSize(80, 80)
        self.color_label.setStyleSheet("""
            background-color: white;
            border: 2px solid #6395EE;
            border-radius: 5px;
        """)
        center_layout.addWidget(self.color_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_area.addLayout(center_layout)

        # Barre du bas : expressions + importer
        bottom_layout = QHBoxLayout()

        expressions = [
            ("😐", "normal", self.on_expression_normal),
            ("😠", "angry", self.on_expression_angry),
            ("🤩", "excited", self.on_expression_excited),
            ("😲", "wide", self.on_expression_wide),
            ("😜", "wiggle", self.on_expression_wiggle),
        ]

        for emoji, name, handler in expressions:
            btn = QPushButton(emoji)
            btn.setToolTip(name)
            btn.setObjectName("btn_expr")
            btn.setFixedSize(70, 70)
            btn.clicked.connect(handler)
            bottom_layout.addWidget(btn)

        bottom_layout.addStretch()

        self.btn_import_dance = QPushButton("Importer .dance")
        self.btn_import_dance.setObjectName("btn_import")
        self.btn_import_dance.clicked.connect(self.import_dance_file)
        bottom_layout.addWidget(self.btn_import_dance)

        main_layout.addLayout(bottom_layout)

        # Timer batterie toutes les 30 secondes
        self.update_battery()
        self.battery_timer = QTimer(self)
        self.battery_timer.timeout.connect(self.update_battery)
        self.battery_timer.start(30000)

        # Timer couleur toutes les secondes
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.on_read_color)
        self.color_timer.start(1000)

    # Méthodes bras
    def on_arm_right_back(self):
        self.marty.move_arm('ARB')

    def on_arm_left_back(self):
        self.marty.move_arm('ALB')

    def on_arm_right_up(self):
        self.marty.move_arm('ARU')

    def on_arm_left_up(self):
        self.marty.move_arm('ALU')

    # Méthodes déplacements 
    def on_forward(self):
        self.marty.move_foot('U', 1)

    def on_left(self):
        self.marty.move_foot('L', 1)

    def on_right(self):
        self.marty.move_foot('R', 1)

    def on_backward(self):
        self.marty.move_foot('B', 1)

    def on_stand(self):
        self.marty.marty.stand_straight(500)

    # Méthodes expressions
    def on_expression_normal(self):
        self.marty.eyes_expression('normal')

    def on_expression_angry(self):
        self.marty.eyes_expression('angry')

    def on_expression_excited(self):
        self.marty.eyes_expression('excited')

    def on_expression_wide(self):
        self.marty.eyes_expression('wide')

    def on_expression_wiggle(self):
        self.marty.eyes_expression('wiggle')

    # Import .dance 
    def import_dance_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importer un fichier dance", "",
            "Fichiers Dance (*.dance);;Tous les fichiers (*)"
        )
        if file_path:
            print(f"Fichier sélectionné : {file_path}")

    # Batterie 
    def update_battery(self):
        try:
            battery = self.marty.getBattery()
            self.battery_label.setText(f"Batterie : {battery}%")
        except:
            self.battery_label.setText("Batterie : N/A")

    # Couleur 
    def on_read_color(self):
        try:
            color_code = self.marty.getColor()
            self.update_color_square(color_code)
        except Exception as e:
            self.color_label.setStyleSheet(
                "background-color: white; border: 2px solid #ff0000; border-radius: 5px;"
            )

    def update_color_square(self, color_code):
        color_map = {
            "N": "#1a1a1a",
            "Y": "#f5c518",
            "G": "#4caf50",
            "R": "#e53935",
            "P": "#9c27b0",
            "C": "#00bcd4"
        }
        color = color_map.get(color_code, "white")
        self.color_label.setStyleSheet(f"""
            background-color: {color};
            border: 2px solid #6395EE;
            border-radius: 5px;
        """)