# Dance Battle — Robotics Application & Referee Server (Python / PyQt)

This project involves the development of a complete "Dance Battle" system for autonomous Marty robots navigating an arena made of colored tiles.

The ecosystem is built upon two distinct applications:

1. **Robot Application (Client GUI):** Parses and executes choreographies from custom `.dance` files, controls the robot's hardware state, and transmits its actions to the server in real-time. It also features a manual piloting mode outside of battles.
2. **Server Application (Referee):** Receives data from the robots via a REST/HTTP API, evaluates their performances based on rule sets defined in a `.battle` file, and calculates live scores.

### Tech Stack

* **Language:** Python 3
* **Graphical Interface:** PyQt6
* **Robotics:** `martypy` library & custom 3D RGB color calibration
* **Network:** HTTP / REST API (JSON data exchange)
* **Environment Management:** Virtual environments (`venv`)

