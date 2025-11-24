# JankenSight

🌟 Rock-Paper-Scissors with Computer Vision (YOLOv8)🎯 

About the ProjectThis is an interactive project that combines computer vision with the classic game Rock, Paper, Scissors (Jokenpô). Using the YOLOv8 object detection model, the system detects your hand movement (your move) in real-time via webcam and plays against an Artificial Intelligence (AI) to determine the winner.
The project serves as a practical and visually appealing demonstration of object detection using Python, leveraging the ultralytics and OpenCV libraries.

⚡ Key Features
- Real-Time Detection: Uses the YOLOv8 model specifically trained to classify Rock, Paper, and Scissors gestures.
- Enhanced OpenCV Interface: A robust graphical interface featuring a prominently placed centralized scoreboard, countdown timer, and interactive buttons (Quit, Pause, Fullscreen).
- Responsive Design: Visual elements (buttons and zones) are positioned to look good across different window sizes.

🛠️ Technologies Used
- Python 3.x
- YOLOv8 (Ultralytics): Deep learning framework for object detection.
- OpenCV (cv2): Camera handling, GUI management, and real-time visualization.

⚙️ Installation and SetupFollow the steps below to set up and run the project on your machine.
1. Clone the Repository
   Open your terminal and clone the project:
   git clone https://github.com/SeuUsuario/jokenpo-yolov8.git
   cd jokenpo-yolov8

3. Install DependenciesIt's recommended to use a virtual environment:
    Create and activate virtual environment: 
---> python -m venv venv
     source venv/bin/activate  # Linux/macOS
     # .\venv\Scripts\activate # Windows


4. Install dependencies
pip install ultralytics opencv-python numpy

5. Configure the ModelThe trained model (best.pt) must be placed in the models/ directory.

jokenpo-yolov8/
├── game.py
├── utils/
│   └── game_logic.py
├── models/
│   └── best.pt  
└── README.md

▶️ How to PlayRun the main file game.py:
  > python game.py

🎮 Interface and ControlsElementFunction
Centralized Scoreboard ---- Displays YOUR and AI scores prominently at the bottom center.
Bottom Zones           ---- Indicate your detection area (left) and the AI's area (right).
Countdown Timer        ---- Shows the time remaining before the next move.

Button           Shortcut            KeyFunction
TELA CHEIA          F           Toggles between windowed and fullscreen mode.
PAUSE/RETOMAR       P           Pauses or resumes the game loop.
SAIR                Q           Quits the application.


🤝 ContributionsContributions, suggestions, and bug reports are welcome! Feel free to open an issue or submit a pull request.
