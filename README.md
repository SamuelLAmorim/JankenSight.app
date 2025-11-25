# 🖐️ JankenSight  
### Rock-Paper-Scissors with Computer Vision (YOLOv8)

---

## 🌟 About the Project  
**JankenSight** is an interactive project that combines **computer vision** with the classic game **Rock, Paper, Scissors (Jokenpô)**.  
Using a **YOLOv8** model trained to recognize hand gestures, the system detects your move in real time via webcam and plays against an AI opponent.

This project is a hands-on and visually appealing demonstration of **object detection using Python**, leveraging the **Ultralytics** and **OpenCV** libraries.

---

## ⚡ Key Features  
- 🎥 **Real-Time Detection** – YOLOv8 classifies Rock, Paper, and Scissors directly from your webcam.  
- 🖼️ **Enhanced OpenCV Interface** – Central scoreboard, countdown timer, and interactive buttons (Quit, Pause, Fullscreen).  
- 📐 **Responsive Layout** – UI elements adapt well to different window sizes.  
- 🧩 **Clean Game Logic** – Organized structure separating interface, model handling, and game rules.

---

## 🛠️ Technologies Used  
- **Python 3.x**  
- **YOLOv8 (Ultralytics)** — Deep learning model for gesture detection  
- **OpenCV (cv2)** — Webcam control, drawing UI, and visualization  
- **NumPy**

---

## ⚙️ Installation and Setup  

### 1. Clone the Repository  

git clone https://github.com/SeuUsuario/jokenpo-yolov8.git
cd jokenpo-yolov8

2. Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate # Windows

3. Install Dependencies
pip install ultralytics opencv-python numpy

4. Place the Model
Ensure your trained model best.pt is inside the models/ directory:

Copy code
jokenpo-yolov8/
├── game.py
├── utils/
│   └── game_logic.py
├── models/
│   └── best.pt
└── README.md
▶️ How to Play
Run the main game file:

python game.py
🎮 Interface and Controls
🧭 Screen Elements
Element	Description
Centralized Scoreboard	Shows your score and the AI's score.
Bottom Zones	Left: your detection area. Right: AI’s area.
Countdown Timer	Time left before the next move.

⌨️ Buttons & Shortcuts
Button / Key	Function
F	Toggle fullscreen
P	Pause / Resume
Q	Quit game

🤝 Contributions
Contributions, suggestions, and bug reports are welcome!
Feel free to open an issue or submit a pull request.
