# VOICE-ASSISTANT-INTEGRATED-ARDUINO-BASED-HOME-AUTOMATION-SYSTEM
🏠 AI-Based Home Automation System using Arduino, ESP32 & Ollama

An AI-powered Smart Home Automation System that combines Voice Control, Web Dashboard, Offline AI Assistant, and IoT-based device control using Arduino UNO, ESP32, and Ollama (Llama 3.2:3B).

📌 Overview

This project demonstrates an intelligent home automation system that enables users to control electrical appliances through:

🎤 Voice Commands
🌐 Web Dashboard
🤖 AI Assistant (Offline)
📟 LCD Display
⚡ ESP32 & Arduino Communication

Unlike traditional home automation systems, this project integrates an offline Large Language Model (LLM) using Ollama (Llama 3.2:3B) to provide conversational AI capabilities while also controlling home appliances.

✨ Features
🏠 Home Automation
Turn Bulb ON/OFF
Turn Fan ON/OFF
Real-time Device Status
LCD Status Display
ESP32 Wi-Fi Communication
Arduino Relay Control
🎤 Voice Assistant
Wake Word Support ("Assistant")
Voice Recognition
Text-to-Speech Responses
Natural Voice Interaction
Local Processing

Example:

Assistant

Turn on bulb

Turning on bulb.
🤖 AI Assistant

Powered by

Ollama
Llama 3.2:3B

Capabilities:

General Question Answering
Date & Time
Mathematical Calculations
General Knowledge
Offline AI Processing

Example:

Assistant

What is Artificial Intelligence?
🌐 Web Dashboard
Device Control
Live Device Status
AI Chat
ESP32 Connection Status
Command History
Responsive Design
📟 LCD Display

Displays

Bulb : ON

Fan : OFF

Automatically updates whenever device status changes.

🏗 System Architecture
                   User
                     │
     ┌───────────────┼────────────────┐
     │               │                │
     ▼               ▼                ▼
Voice Assistant   Web Dashboard    AI Chat
     │               │                │
     └───────────────┼────────────────┘
                     ▼
              Python Application
                     │
     ┌───────────────┼───────────────┐
     │               │               │
     ▼               ▼               ▼
Speech         Flask Server      Ollama AI
Recognition                      (Llama3.2)
                     │
                     ▼
               Serial Communication
                     │
                     ▼
                 ESP32 DevKit
                     │
                     ▼
                Arduino UNO
             ┌────────┴────────┐
             ▼                 ▼
        Relay Module      LCD Display
             │
             ▼
       Bulb & Fan
🛠 Hardware Components
Arduino UNO R3
ESP32 DevKit V1
2-Channel Relay Module
16×2 LCD Display (I2C)
Breadboard
Jumper Wires
USB Cables
LED Bulb / Lamp
DC Fan
💻 Software Requirements
Python 3.11+
Arduino IDE
Visual Studio Code
Ollama
Llama 3.2:3B Model
📚 Python Libraries

Install dependencies using:

pip install flask
pip install pyserial
pip install SpeechRecognition
pip install pyaudio
pip install requests
pip install pygame
pip install edge-tts
🤖 Install Ollama

Download Ollama

https://ollama.com

Install Llama 3.2

ollama pull llama3.2:3b

Run the model

ollama run llama3.2:3b
📂 Project Structure
HomeAutomation/

│

├── app.py

├── config.py

├── templates/

│      index.html

│

├── static/

│      style.css

│      script.js

│

├── Arduino/

│      Arduino.ino

│

├── ESP32/

│      ESP32.ino

│

└── README.md
🚀 How to Run
Step 1

Upload Arduino code.

Step 2

Upload ESP32 code.

Step 3

Run Ollama

ollama run llama3.2:3b
Step 4

Start Python

python app.py
Step 5

Open Browser

http://127.0.0.1:5000
🎤 Voice Commands
Assistant

Turn on bulb

Turn off bulb

Turn on fan

Turn off fan

What is AI?

What is the time?

What is today's date?

300 × 400

Go to sleep
🌐 Website Features
Bulb Control
Fan Control
AI Chat
Live Status
Command History
ESP32 Status
Date & Time
🔄 Project Workflow
Voice Command

↓

Speech Recognition

↓

Python Application

↓

ESP32

↓

Arduino UNO

↓

Relay Module

↓

Bulb/Fan

↓

LCD Update

↓

Website Update
📈 Future Enhancements
Motion Detection
Fingerprint Authentication
Face Recognition
Smart Energy Monitoring
Weather Integration
Mobile Application
Additional Smart Devices
MQTT Support
🎯 Key Highlights
Offline AI using Ollama
Voice-controlled Home Automation
Web-based Device Management
Real-time Status Synchronization
ESP32 + Arduino Integration
LCD Status Monitoring
Local AI Processing
Modular Architecture
Scalable Design
👨‍💻 Author

Avinash Reddy
B.Tech – Artificial Intelligence & Machine Learning
Amity University Bengaluru
