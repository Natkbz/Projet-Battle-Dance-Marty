class MartyController:

    def connect(self, ip: str) -> bool:
        """Connexion au robot. Renvoie True si succès, False sinon."""
        # Remplacer ce code par la vraie connexion au Marty
        print(f"Tentative de connexion à {ip}...")
        return True  # simulation d'une connexion réussie pour l'instant pour test

    def disconnect(self):
        """Déconnexion du robot."""
        print("Déconnexion du robot")

    def move_forward(self):
        print("Avancer")

    def move_backward(self):
        print("Reculer")

    def move_left(self):
        print("Gauche")

    def move_right(self):
        print("Droite")

    def get_battery(self) -> int:
        """Renvoie le niveau de batterie en %."""
        return 75  # test

    def get_floor_color(self) -> str:
        """Renvoie la couleur détectée au sol."""
        return "N"  # test