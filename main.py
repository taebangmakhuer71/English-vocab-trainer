import tkinter as tk
import random
from fileinput import filename

import speech_recognition as sr
import pyttsx3
from PIL import Image, ImageTk
import os

# ตั้งค่าระบบพูด
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# พูดภาษาอังกฤษ
def speak(text):
    engine.say(text)
    engine.runAndWait()

# รายการคำศัพท์
vocab_list = ["cat", "dog", "rabbit", "hamster", "bird", "fish", "turtle", "lion", "tiger", "monkey",
              "elephant", "giraffe", "bear", "wolf", "deer", "snake", "koala", "panda", "fox", "pig",

              "calendar", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "january", "february",
              "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",

              "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
              "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eightteen", "nineteen", "twenty",

              "red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "white",
              "gray", "silver", "gold", "school", "what", "do", "have", "can", "like", "read",

              "with", "at", "look", "out", "up", "very", "down", "sit", "jump", "hat",
              "here", "where", "home", "pull", "good", "come", "pet", "big", "sad", "class"]

score = 0
current_word = ""

# ฟังก์ชันสุ่มคำศัพท์ใหม่
def next_word():
    global current_word
    current_word = random.choice(vocab_list)
    word_label.config(text=current_word)
    speak(f"Please say: {current_word}")
    result_label.config(text="")

# ฟังก์ชันฟังเสียง
def recognize_speech():
    global score
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say the word now")
        result_label.config(text="กำลังฟัง...")
        window.update()
        try:
            audio = recognizer.listen(source, timeout=3)
            spoken_word = recognizer.recognize_google(audio)
            print("คุณพูดว่า:", spoken_word)

            if spoken_word.lower() == current_word.lower():
                result_label.config(text="✅ ถูกต้อง! เก่งมาก", fg="green")
                speak("Correct! Great job!")
                score += 1
            else:
                result_label.config(text=f"❌ ไม่ถูก ลองใหม่นะ (คุณพูดว่า: {spoken_word})", fg="red")
                speak("That's not correct. Try again.")

            score_label.config(text=f"คะแนน: {score}")
        except sr.UnknownValueError:
            result_label.config(text="❗ ฟังไม่ชัด ลองพูดใหม่อีกครั้ง", fg="orange")
            speak("Sorry, I couldn't understand.")
        except sr.RequestError:
            result_label.config(text="❗ เกิดข้อผิดพลาดในการเชื่อมต่อ", fg="red")
            speak("Error connecting to the recognition service.")
        except sr.WaitTimeoutError:
            result_label.config(text="⏰ พูดช้าไป ลองใหม่", fg="blue")
            speak("You took too long. Try again.")
# เริ่มใหม่
def restart_game():
    global score, word_index
    score = 0
    word_index = 0
    score_label.config(text="คะแนน: 0")
    result_label.config(text="")
    next_word()

# สร้าง GUI
window = tk.Tk()
window.title("🎓 AI ฝึกพูดคำศัพท์ภาษาอังกฤษ")
window.geometry("500x600")
window.config(bg="#d0f0ff")

# ภาพตกแต่ง
bg_image = Image.open ("main.png")
bg_image = bg_image.resize((500,600))
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(window, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# องค์ประกอบหน้าจอ
title_label = tk.Label(window, text="🗣️ ฝึกพูดคำศัพท์ภาษาอังกฤษ", font=("Comic Sans MS", 20, "bold"), bg="#d0f0ff", fg="#004080")
title_label.pack(pady=15)

current_word = tk.StringVar()
word_label = tk.Label(window, text="", font=("Arial", 40, "bold"), bg="#d0f0ff", fg="#3333cc")
word_label.pack(pady=10)

image_label = tk.Label(window, bg="#d0f0ff")
image_label.pack(pady=10)

speak_button = tk.Button(window, text="🎤 พูดคำศัพท์", font=("Arial", 16), bg="#80dfff", fg="black", width=20, command=recognize_speech)
speak_button.pack(pady=10)

next_button = tk.Button(window, text="➡️ คำถัดไป", font=("Arial", 12), bg="#b3e6ff", command=next_word)
next_button.pack(pady=5)

restart_button = tk.Button(window, text="🔄 เริ่มใหม่", font=("Arial", 12), bg="#b3e6ff", command=restart_game)
restart_button.pack(pady=5)

result_label = tk.Label(window, text="", font=("Arial", 14), bg="#d0f0ff")
result_label.pack(pady=10)

score_label = tk.Label(window, text="คะแนน: 0", font=("Arial", 12), bg="#d0f0ff")
score_label.pack(pady=5)

footer = tk.Label(window, text="By Phumin & Sittinon", font=("Arial", 9), bg="#d0f0ff", fg="#666")
footer.pack(side="bottom", pady=10)

# เริ่มเกม
next_word()
window.mainloop()