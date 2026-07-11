# ==========================================
# HOME AUTOMATION WITH AI ASSISTANT
# Main Application
# ==========================================

import threading
import time
import serial
import requests
import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import tempfile
import os

from datetime import datetime
from flask import Flask, render_template, request, jsonify

import config
chat_history=[]
# ==========================================
# GLOBAL VARIABLES
# ==========================================

bulb_status = config.DEFAULT_BULB
fan_status = config.DEFAULT_FAN
conversation=[]

# ==========================================
# COMMAND HISTORY
# ==========================================

command_history = []

SYSTEM_PROMPT = """
You are HomeAI.

Rules:

1. Answer directly.
2. Never add extra conversation.
3. Never ask follow-up questions.
4. Never say "Would you like..."
5. Never say "Now..."
6. Maximum 2 sentences.
7. If the question has a single factual answer, reply with only that answer.
8. If it is a math question, return only the calculation result.
9. Be concise and professional.
"""

esp = None
esp_connected = False

serial_lock = threading.Lock()
# Wake session

assistant_awake = False


# ==========================================
# FLASK
# ==========================================

app = Flask(__name__)

# ==========================================
# SPEECH RECOGNIZER
# ==========================================

recognizer = sr.Recognizer()

# ==========================================
# SPEAK FUNCTION
# ==========================================

VOICE="en-IN-NeerjaNeural"

async def speak_async(text):

    communicate=edge_tts.Communicate(text,VOICE)

    temp=tempfile.NamedTemporaryFile(delete=False,suffix=".mp3")

    filename=temp.name

    temp.close()

    await communicate.save(filename)

    pygame.mixer.init()

    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        await asyncio.sleep(0.1)

    pygame.mixer.quit()

    os.remove(filename)


def speak(text):

    asyncio.run(speak_async(text))
# ==========================================
# SAVE COMMAND HISTORY
# ==========================================

def log_command(source, command):

    global command_history

    command_history.append({

        "time": datetime.now().strftime("%I:%M:%S %p"),

        "source": source,

        "command": command

    })

    # Keep only last 20 commands

    if len(command_history) > 20:

        command_history.pop(0)

# ==========================================
# CONNECT ESP32
# ==========================================

def connect_esp():

    global esp
    global esp_connected

    while True:

        try:

            esp = serial.Serial(
                config.COM_PORT,
                config.BAUD_RATE,
                timeout=1
            )

            time.sleep(2)

            print("\nESP32 Connected Successfully\n")
            esp_connected = True

            return

        except Exception as e:

            print("Waiting for ESP32...")

            print(e)

            time.sleep(2)
            esp_connected = False

# ==========================================
# SEND COMMAND
# ==========================================

def send_command(command):

    global esp

    global bulb_status

    global fan_status

    try:

        if esp is None or not esp.is_open:

            connect_esp()

        with serial_lock:

            esp.write((command + "\n").encode())

            esp.flush()

        print("Sent ->", command)

        log_command("ESP32", command)

        if command == "BULB_ON":

            bulb_status = "ON"

        elif command == "BULB_OFF":

            bulb_status = "OFF"

        elif command == "FAN_ON":

            fan_status = "ON"

        elif command == "FAN_OFF":

            fan_status = "OFF"

    except Exception as e:

        print("Serial Error :", e)

        connect_esp()

# ==========================================
# READ ESP32
# ==========================================

def serial_reader():

    global bulb_status

    global fan_status

    while True:

        try:

            if esp is not None and esp.in_waiting:

                message = esp.readline().decode().strip()

                print("ESP32 :", message)

                if "B:ON" in message:

                    bulb_status = "ON"

                elif "B:OFF" in message:

                    bulb_status = "OFF"

                if "F:ON" in message:

                    fan_status = "ON"

                elif "F:OFF" in message:

                    fan_status = "OFF"

        except Exception as e:

            print(e)

        time.sleep(0.1)

# ==========================================
# DATE & TIME
# ==========================================

def get_time():
    return datetime.now().strftime("%I:%M %p")


def get_date():
    return datetime.now().strftime("%d %B %Y")


# ==========================================
# OLLAMA
# ==========================================

# ==========================================
# OLLAMA (Llama3.2:3B)
# ==========================================

def ask_ollama(prompt):

    global conversation

    try:

        conversation.append({
            "role": "user",
            "content": prompt
        })

        payload = {

             "model": config.OLLAMA_MODEL,

             "messages": [

                {
                   "role": "system",
                   "content": SYSTEM_PROMPT
             }

             ] + conversation,

             "stream": False,

             "options": {

                "temperature": 0.5,

                 "num_predict": 80,

                 "top_k": 20,

                 "top_p": 0.8

             }

         }

        response = requests.post(

            "http://localhost:11434/api/chat",

            json=payload,

            timeout=120

        )

        response.raise_for_status()

        data = response.json()

        if "message" not in data:

            print(data)

            return "Invalid response received from Ollama."

        answer = data["message"]["content"]

        conversation.append({

            "role": "assistant",

            "content": answer

        })

        log_command("AI", answer)

        return answer

    except requests.exceptions.ConnectionError:

        return "Ollama server is not running."

    except requests.exceptions.Timeout:

        return "Ollama is taking too long to respond."

    except Exception as e:

        print("OLLAMA ERROR")

        print(e)

        return "AI Error occurred."
    

# ==========================================
# VOICE ASSISTANT
# ==========================================

def voice_assistant():

    global bulb_status
    global fan_status
    global assistant_awake

    recognizer = sr.Recognizer()

    print("\nVoice Assistant Ready\n")

    while True:

        try:

            with sr.Microphone(device_index=config.MICROPHONE_INDEX) as source:

                print("\nListening...")

                recognizer.adjust_for_ambient_noise(source, duration=0.8)

                audio = recognizer.listen(source)

            print("Recognizing...")

            command = recognizer.recognize_google(audio)

            command = command.lower()

            print("You :", command)

            log_command("Voice", command)

# ---------------------------------
# WAKE SESSION
# ---------------------------------

            if not assistant_awake:

               if command == "assistant":

                assistant_awake = True
 
                speak("Yes, I am listening.")

                continue        # <-- VERY IMPORTANT

               else:

                continue

# ---------------------------------
# MANUAL SLEEP
# ---------------------------------

            if command in ["go to sleep", "stop listening", "goodbye"]:

             assistant_awake = False

             speak("Okay. Going to sleep.")

             continue
            # ---------------- Bulb ----------------

            if "turn on bulb" in command or "bulb on" in command:

                send_command("BULB_ON")

                speak("Turning on bulb")

            elif "turn off bulb" in command or "bulb off" in command:

                send_command("BULB_OFF")

                speak("Turning off bulb")

            # ---------------- Fan ----------------

            elif "turn on fan" in command or "fan on" in command:

                send_command("FAN_ON")

                speak("Turning on fan")

            elif "turn off fan" in command or "fan off" in command:

                send_command("FAN_OFF")

                speak("Turning off fan")

            # ---------------- Status ----------------

            elif "status" in command:

                speak(f"Bulb is {bulb_status}")

                speak(f"Fan is {fan_status}")

            # ---------------- Time ----------------

            elif "time" in command:

                speak(f"The current time is {get_time()}")

            # ---------------- Date ----------------

            elif "date" in command:

                speak(f"Today's date is {get_date()}")

            # ---------------- Exit ----------------

            elif "exit" in command or "stop assistant" in command:

                speak("Goodbye")

                break

            # ---------------- AI ----------------

            else:

                print("\nSending to Ollama...")

                speak("let me think.")

                answer = ask_ollama(command)

                print("\n========== AI ==========")
                print(answer)
                print("========================\n")

                speak(answer)
        except sr.UnknownValueError:

            print("Could not understand.")

        except sr.RequestError as e:

            print("Speech Recognition Error:", e)

        except Exception as e:

            print("Voice Assistant Error:", e)
            
def listen_command():

    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=config.MICROPHONE_INDEX) as source:

        print("Waiting for command...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        audio = recognizer.listen(source)

    command = recognizer.recognize_google(audio)

    command = command.lower()

    print("Command :", command)

    return command            
# ==========================================
# FLASK ROUTES
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/status")
def status():
    return jsonify({
        "bulb": bulb_status,
        "fan": fan_status
    })


@app.route("/bulb/on", methods=["GET"])
def bulb_on():

    send_command("BULB_ON")

    return jsonify({
        "status": "success",
        "bulb": bulb_status,
        "fan": fan_status
    })


@app.route("/bulb/off", methods=["GET"])
def bulb_off():

    send_command("BULB_OFF")

    return jsonify({
        "status": "success",
        "bulb": bulb_status,
        "fan": fan_status
    })


@app.route("/fan/on", methods=["GET"])
def fan_on():

    send_command("FAN_ON")

    return jsonify({
        "status": "success",
        "bulb": bulb_status,
        "fan": fan_status
    })


@app.route("/fan/off", methods=["GET"])
def fan_off():

    send_command("FAN_OFF")

    return jsonify({
        "status": "success",
        "bulb": bulb_status,
        "fan": fan_status
    })


@app.route("/device/status")
def device_status():

    return jsonify({

"bulb":bulb_status,

"fan":fan_status,

"time":get_time(),

"date":get_date(),

"connected":esp_connected,

"history":command_history[-10:],

"chat":chat_history

})
# ==========================================
# AI CHAT API
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        prompt = data.get("message", "")

        reply = ask_ollama(prompt)

        return jsonify({

            "reply": reply

        })

    except Exception as e:

        return jsonify({

            "reply": str(e)

        })

if __name__ == "__main__":

    connect_esp()

    threading.Thread(
        target=serial_reader,
        daemon=True
    ).start()

    threading.Thread(
        target=voice_assistant,
        daemon=True
    ).start()

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=False,
        use_reloader=False
    )
