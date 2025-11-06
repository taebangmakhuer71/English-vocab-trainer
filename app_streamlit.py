import streamlit as st
import random
import speech_recognition as sr
import base64  # <<<<<<<<<< เพิ่มบรรทัดนี้ <<<<<<<<<<


# (1) ลบ Tkinter, pyttsx3, PIL ออก
# pyttsx3, PIL, และ Tkinter ไม่ทำงานบนเว็บเซิร์ฟเวอร์

# (2) ฟังก์ชันพูด (Speak) - ปรับเปลี่ยน
# ใน Web App เราจะใช้การแสดงข้อความแจ้งเตือนแทนการพูดจริง
def speak(text):
    """ฟังก์ชันนี้ใช้แสดงข้อความที่ระบบควรจะพูด"""
    st.info(f"ระบบพูด: {text}")


# (3) รายการคำศัพท์ (ใช้เดิม)
# คัดลอก vocab_list ของคุณมาใส่ตรงนี้
vocab_list = ["cat", "dog", "rabbit", "hamster", "bird", "fish", "turtle", "lion", "tiger", "monkey",
              "elephant", "giraffe", "bear", "wolf", "deer", "snake", "koala", "panda", "fox", "pig",
              "calendar", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "january",
              "february",
              "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
              "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
              "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eightteen", "nineteen",
              "twenty",
              "red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "white",
              "gray", "silver", "gold", "school", "what", "do", "have", "can", "like", "read",
              "with", "at", "look", "out", "up", "very", "down", "sit", "jump", "hat",
              "here", "where", "home", "pull", "good", "come", "pet", "big", "sad", "class"]

# (4) การจัดการสถานะ (State Management)
# ใน Streamlit เราใช้ st.session_state แทน global variables
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_word' not in st.session_state:
    st.session_state.current_word = ""
if 'result_text' not in st.session_state:
    st.session_state.result_text = ""
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False


# ฟังก์ชันสุ่มคำศัพท์ใหม่ (Logic เดิม)
def next_word():
    st.session_state.current_word = random.choice(vocab_list)
    speak(f"Please say: {st.session_state.current_word}")
    st.session_state.result_text = ""
    st.session_state.is_listening = False


# ฟังก์ชันเริ่มเกมใหม่ (Logic เดิม)
def restart_game():
    st.session_state.score = 0
    st.session_state.result_text = ""
    st.session_state.is_listening = False
    next_word()


# ฟังก์ชันฟังเสียง (ปรับเปลี่ยนเพื่อรับข้อความแทน)
def recognize_speech_web(user_input):
    """จำลองการรับเสียงโดยรับข้อความจากผู้ใช้และตรวจสอบคำ"""
    if not user_input:
        st.session_state.result_text = "กรุณาพิมพ์คำศัพท์ที่ได้ยิน"
        return

    spoken_word = user_input.lower().strip()
    current = st.session_state.current_word.lower()

    # ตรวจสอบคำศัพท์ (Logic เดิม)
    if spoken_word == current:
        st.session_state.result_text = "✅ ถูกต้อง! เก่งมาก"
        speak("Correct! Great job!")
        st.session_state.score += 1
    else:
        st.session_state.result_text = f"❌ ไม่ถูก ลองใหม่นะ (คุณพิมพ์ว่า: {spoken_word})"
        speak("That's not correct. Try again.")

    st.session_state.is_listening = False


# ==============================================================================
# 5. สร้าง Streamlit UI (แทนที่ GUI Tkinter)
# ==============================================================================

st.set_page_config(page_title="ฝึกพูดคำศัพท์", layout="centered")

# <<<<<<<<<< เพิ่มโค้ด CSS สำหรับรูปภาพพื้นหลังและ Style อื่นๆ ตรงนี้ <<<<<<<<<<
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64.b64encode(open('main.png', 'rb').read()).decode()}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #3333cc; /* ปรับสีตัวอักษรให้เข้ากับพื้นหลัง */
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: #004080; /* สีเดียวกับ title_label เดิม */
        text-align: center;
    }}
    .stButton>button {{
        background-color: #80dfff; /* สีเดียวกับปุ่มเดิม */
        color: black;
        border-radius: 5px;
        border: 1px solid #80dfff;
        font-size: 16px; /* ปรับขนาดตัวอักษรปุ่ม */
        padding: 10px 20px; /* เพิ่มพื้นที่ในปุ่ม */
        margin: 5px 0; /* เพิ่มระยะห่างระหว่างปุ่ม */
    }}
    .stTextInput>div>div>input {{
        border-radius: 5px;
        border: 1px solid #b3e6ff;
        background-color: white;
        color: black;
        padding: 10px;
    }}
    .stAlert {{
        border-radius: 5px;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# <<<<<<<<<< สิ้นสุดส่วนที่เพิ่ม <<<<<<<<<<


# องค์ประกอบหน้าจอ
st.markdown("<h1 style='text-align: center; color: #004080;'>🗣️ AI ฝึกพูดคำศัพท์ภาษาอังกฤษ</h1>",
            unsafe_allow_html=True)

# แสดงคำศัพท์
st.markdown(
    f"<h2 style='text-align: center; font-size: 40px; color: #3333cc;'>**{st.session_state.current_word.upper()}**</h2>",
    unsafe_allow_html=True)

# พื้นที่สำหรับปุ่ม "พูดคำศัพท์" ตรงกลาง
speak_col = st.columns([1, 2, 1])  # ทำให้ปุ่มอยู่ตรงกลาง
with speak_col[1]:
    if st.button("🎤 เริ่มพูด (หรือพิมพ์)", key="speak_main", use_container_width=True):
        st.session_state.is_listening = True

# ปุ่ม "คำถัดไป" และ "เริ่มใหม่"
col1, col2 = st.columns(2)
with col1:
    if st.button("➡️ คำถัดไป", key="next", use_container_width=True):
        next_word()
        st.rerun()
with col2:
    if st.button("🔄 เริ่มใหม่", key="restart", use_container_width=True):
        restart_game()
        st.rerun()

# ส่วนฝึกพูด (พิมพ์คำที่คุณพูด)
st.markdown("---")
st.subheader("ส่วนฝึกพูด (พิมพ์คำที่คุณพูด):")

if st.session_state.is_listening:
    # ช่องกรอกข้อความแทนไมโครโฟน
    user_input = st.text_input("พิมพ์คำศัพท์ที่คุณคิดว่าได้ยิน:", key="speech_input")

    # ปุ่มตรวจสอบคำพูด
    if st.button("ตรวจสอบคำพูด", key="check_speech", use_container_width=True):
        recognize_speech_web(user_input)
        # st.rerun() เพื่ออัปเดตผลลัพธ์ทันทีหลังตรวจสอบ
        st.rerun()
else:
    # เคลียร์ช่องพิมพ์เมื่อไม่ได้อยู่ในโหมด 'Listening'
    pass

# (7) แสดงผลลัพธ์
if st.session_state.result_text:
    if st.session_state.result_text.startswith("✅"):
        st.success(st.session_state.result_text)
    elif st.session_state.result_text.startswith("❌"):
        st.error(st.session_state.result_text)
    elif st.session_state.result_text.startswith("ระบบพูด:"):
        # แสดง st.info ให้ตรงกับคำสั่ง speak()
        st.info(st.session_state.result_text)
    else:
        st.warning(st.session_state.result_text)

# แสดงคะแนน (ปรับมาอยู่ด้านล่างหลัก)
st.markdown(f"<h3 style='text-align: center;'>คะแนน: {st.session_state.score}</h3>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 10px; color: #666;'>By Phumin & Sittinon</p>",
            unsafe_allow_html=True)

# (8) เริ่มเกมครั้งแรก
if st.session_state.current_word == "":
    next_word()
    st.rerun()