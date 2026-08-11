# Projet 3A Robot

Projet robotique 3A
# Dance Battle — Application Robotique & Serveur d'Arbitrage (Python / PyQt)

Ce projet consiste à développer un système complet de "Dance Battle" pour robots Marty autonomes évoluant dans une arène à dalles colorées.

Le système repose sur deux applications distinctes :
1) L'application Robot (Client GUI) exécute une chorégraphie lue depuis un fichier `.dance`, contrôle l'état du robot et envoie en temps réel ses actions au serveur. On peut aussi le piloter manuellement hors battle
2) L'application Serveur (Arbitre) reçoit les données des robots via une API REST/HTTP, évalue les performances selon des règles défini par un fichier `.battle`, et calcule les scores.

## Technique
* **Langage :** Python 3
* **Interface Graphique :** PyQt6
* **Robotique :** Librairie `martypy`
* **Réseau :** API HTTP / REST (échange de données au format JSON)
* **Gestion d'environnement :** Environnements virtuels (`venv`)

