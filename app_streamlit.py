import streamlit as st
import random
import speech_recognition as sr
import base64
from streamlit.components.v1 import html  # <<< สำหรับฝังโค้ด JavaScript


# ==============================================================================
# 1. ฟังก์ชันการทำงานเกี่ยวกับเสียง (TTS)
# ==============================================================================

# ฟังก์ชัน JavaScript TTS (อ่านออกเสียง)
def play_text_to_speech(text):
    """ใช้ JavaScript เพื่อสั่งให้เบราว์เซอร์ของผู้ใช้พูดข้อความ"""
    safe_text = text.replace("'", "\\'")
    js_code = f"""
    <script>
        var utterance = new SpeechSynthesisUtterance('{safe_text}');
        utterance.lang = 'en-US';
        utterance.rate = 0.9; 
        window.speechSynthesis.speak(utterance);
    </script>
    """
    html(js_code, height=0, width=0)


# ฟังก์ชันพูด (Speak) ที่เรียกใช้ TTS
def speak(text):
    st.info(f"ระบบพูด: {text}")
    play_text_to_speech(text)


# ==============================================================================
# 2. รายการคำศัพท์ และ Logic หลัก
# ==============================================================================

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

# การจัดการสถานะ (State Management)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_word' not in st.session_state:
    st.session_state.current_word = ""
if 'result_text' not in st.session_state:
    st.session_state.result_text = ""
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False


# ฟังก์ชันสุ่มคำศัพท์ใหม่
def next_word():
    st.session_state.current_word = random.choice(vocab_list)
    speak(f"Please say: {st.session_state.current_word}")
    st.session_state.result_text = ""
    st.session_state.is_listening = False


# ฟังก์ชันเริ่มเกมใหม่
def restart_game():
    st.session_state.score = 0
    st.session_state.result_text = ""
    st.session_state.is_listening = False
    next_word()


# ฟังก์ชันตรวจสอบคำศัพท์ (ใช้การพิมพ์แทนไมค์)
def recognize_speech_web(user_input):
    if not user_input:
        st.session_state.result_text = "กรุณาพิมพ์คำศัพท์ที่ได้ยิน"
        return

    spoken_word = user_input.lower().strip()
    current = st.session_state.current_word.lower()

    if spoken_word == current:
        st.session_state.result_text = "✅ ถูกต้อง! เก่งมาก"
        speak("Correct! Great job!")
        st.session_state.score += 1
    else:
        st.session_state.result_text = f"❌ ไม่ถูก ลองใหม่นะ (คุณพิมพ์ว่า: {spoken_word})"
        speak("That's not correct. Try again.")

    st.session_state.is_listening = False


# ==============================================================================
# 3. สร้าง Streamlit UI (พร้อม CSS และ Layout)
# ==============================================================================

st.set_page_config(page_title="ฝึกพูดคำศัพท์", layout="centered")

# โค้ด CSS สำหรับรูปภาพพื้นหลังและ Style ต่างๆ
try:
    with open('main.png', 'rb') as f:
        img_data = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    img_data = ""

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #3333cc;
    }}
    /* สไตล์อื่นๆ */
    h1, h2, h3, h4, h5, h6 {{color: #004080; text-align: center;}}
    .stButton>button {{
        background-color: #80dfff; color: black; border-radius: 5px; border: 1px solid #80dfff;
        font-size: 16px; padding: 10px 20px; margin: 5px 0;
    }}
    .stTextInput>div>div>input {{
        border-radius: 5px; border: 1px solid #b3e6ff; background-color: white;
        color: black; padding: 10px;
    }}
    .stAlert {{border-radius: 5px; text-align: center;}}
    </style>
    """,
    unsafe_allow_html=True
)

# องค์ประกอบหน้าจอหลัก
st.markdown("<h1 style='text-align: center; color: #004080;'>🗣️ AI ฝึกพูดคำศัพท์ภาษาอังกฤษ</h1>",
            unsafe_allow_html=True)
st.markdown(
    f"<h2 style='text-align: center; font-size: 40px; color: #3333cc;'>**{st.session_state.current_word.upper()}**</h2>",
    unsafe_allow_html=True)

# ปุ่ม "เริ่มพูด"
speak_col = st.columns([1, 2, 1])
with speak_col[1]:
    # ปุ่มนี้จะเปลี่ยนโหมดให้แสดงช่องพิมพ์ข้อความ
    if st.button("🎤 พูดคำศัพท์ (กดแล้วพิมพ์คำที่ได้ยิน)", key="speak_main", use_container_width=True):
        st.session_state.is_listening = True

# ปุ่มควบคุมเกม
col1, col2 = st.columns(2)
with col1:
    if st.button("➡️ คำถัดไป", key="next", use_container_width=True):
        next_word()
        st.rerun()
with col2:
    if st.button("🔄 เริ่มใหม่", key="restart", use_container_width=True):
        restart_game()
        st.rerun()

# ส่วนฝึกพูด (การพิมพ์แทนไมค์)
st.markdown("---")
st.subheader("ส่วนฝึกพูด (พิมพ์คำที่คุณพูด):")

if st.session_state.is_listening:
    user_input = st.text_input("พิมพ์คำศัพท์ที่คุณคิดว่าได้ยิน:", key="speech_input")

    if st.button("ตรวจสอบคำพูด", key="check_speech", use_container_width=True):
        recognize_speech_web(user_input)
        st.rerun()
else:
    pass

# แสดงผลลัพธ์
if st.session_state.result_text and not st.session_state.result_text.startswith("ระบบพูด:"):
    if st.session_state.result_text.startswith("✅"):
        st.success(st.session_state.result_text)
    elif st.session_state.result_text.startswith("❌"):
        st.error(st.session_state.result_text)
    else:
        st.warning(st.session_state.result_text)

# แสดงคะแนน
st.markdown(f"<h3 style='text-align: center;'>คะแนน: {st.session_state.score}</h3>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 10px; color: #666;'>By Phumin & Sittinon</p>",
            unsafe_allow_html=True)

# เริ่มเกมครั้งแรก
if st.session_state.current_word == "":
    next_word()
    st.rerun()