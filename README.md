# 🛡️ AI Security Surveillance System

An AI-powered surveillance system that detects people, identifies known faces, and logs intrusion events with captured image evidence.

---

## 🚀 Features

- Real-time person detection (YOLOv8)
- Face recognition for known individuals
- Unknown intrusion detection
- Automatic image capture on intrusion
- Event-based video recording (stored locally)
- SQLite database logging
- Streamlit dashboard for monitoring alerts

---

## 🧠 System Flow

Camera Feed  
→ Person Detection (YOLOv8)  
→ Tracking (ByteTrack)  
→ Face Recognition  
→ Intrusion Detection  
→ Image + Video Capture  
→ Database Logging  
→ Streamlit Dashboard  

---

## 🛠️ Tech Stack

Python, OpenCV, Ultralytics YOLOv8, face_recognition (dlib), Streamlit, SQLite, NumPy, Pandas

---

## 📁 Project Structure

```
ai_security_system/
│
├── app.py                  # Dashboard
├── main.py                 # Surveillance system
│
├── alerts/
│   ├── alert_manager.py
│   ├── video_recorder.py
│   ├── unknown/            # Saved intrusion images
│   └── videos/             # Saved intrusion videos
│
├── detection/
│   └── person_detection.py
│
├── recognition/
│   └── face_recog.py
│
├── tracking/
│   ├── tracker.py
│   └── track_manager.py
│
├── database/
│   └── database_manager.py
│
├── known_faces/            # Authorized faces
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai_security_surveillance_system.git
cd ai_security_surveillance_system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run

Start surveillance system:

```bash
python main.py
```

Run dashboard:

```bash
streamlit run app.py
```

---

## 📊 Dashboard

- Displays real-time alert logs
- Shows captured intrusion images
- Tracks total and daily alerts

---

## ⚠️ Notes

- Video evidence is stored locally in `alerts/videos/`
- Large files (videos, images, database) are excluded via `.gitignore`

---

## 👨‍💻 Author

Developed as part of a Computer Vision / AI Security project.
