import streamlit as st
import random
import speech_recognition as sr
import base64
from streamlit.components.v1 import html
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase  # <<< เพิ่ม Import webrtc


# ==============================================================================
# 1. ฟังก์ชันการทำงานเกี่ยวกับเสียง (TTS และ SR Processor)
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


# ฟังก์ชันถอดรหัสเสียง (Logic เดิม)
def process_speech(audio_data):
    """ใช้ speech_recognition ถอดรหัสเสียงที่ได้รับจากไมโครโฟน"""
    try:
        r = sr.Recognizer()
        # ใช้ recognize_google ในการถอดรหัสเสียง
        spoken_word = r.recognize_google(audio_data, language="en-US")

        current = st.session_state.current_word.lower()
        if spoken_word.lower() == current:
            st.session_state.result_text = "✅ ถูกต้อง! เก่งมาก"
            st.session_state.score += 1
        else:
            st.session_state.result_text = f"❌ ไม่ถูก ลองใหม่นะ (คุณพูดว่า: {spoken_word})"

        speak("Result checked.")  # พูดผลลัพธ์
        st.session_state.is_listening = False
        st.rerun()

    except sr.UnknownValueError:
        st.session_state.result_text = "❌ ไม่ชัด ฟังไม่รู้เรื่อง ลองพูดอีกครั้ง"
    except sr.RequestError:
        st.session_state.result_text = "❌ เกิดข้อผิดพลาดในการเชื่อมต่อบริการถอดรหัสเสียง"
    except Exception as e:
        st.session_state.result_text = f"❌ Error: {e}"


# Processor สำหรับ WebRTC (จำเป็นต้องมีเพื่อดักจับ Audio Chunk)
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        # ใช้เพื่อบันทึก Audio data ที่กำลังเข้ามา
        self.audio_chunks = []
        self.recognizer = sr.Recognizer()

    def recv(self, frame):
        # รับข้อมูลเสียงจากไมโครโฟนของผู้ใช้
        self.audio_chunks.append(frame)
        return frame


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
if 'webrtc_state' not in st.session_state:
    st.session_state.webrtc_state = None


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


# ==============================================================================
# 3. สร้าง Streamlit UI (พร้อม WebRTC)
# ==============================================================================

st.set_page_config(page_title="ฝึกพูดคำศัพท์", layout="centered")

# โค้ด CSS สำหรับรูปภาพพื้นหลังและ Style ต่างๆ (เหมือนเดิม)
try:
    with open('main.png', 'rb') as f:
        img_data = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    img_data = ""

# ... (โค้ด CSS สไตล์ต่างๆ เหมือนเดิม) ...
st.markdown(
    f"""
    <style>
    .stApp {{ background-image: url("data:image/png;base64,{img_data}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; color: #3333cc;}}
    h1, h2, h3, h4, h5, h6 {{color: #004080; text-align: center;}}
    .stButton>button {{ background-color: #80dfff; color: black; border-radius: 5px; border: 1px solid #80dfff; font-size: 16px; padding: 10px 20px; margin: 5px 0; }}
    .stTextInput>div>div>input {{ border-radius: 5px; border: 1px solid #b3e6ff; background-color: white; color: black; padding: 10px; }}
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

# -------------------------------------------------------------
# ส่วนฝึกพูด (ใช้ไมโครโฟน WebRTC)
# -------------------------------------------------------------
st.markdown("---")
st.subheader("🎤 ส่วนฝึกพูด (พูดคำศัพท์):")

# ปุ่ม 'เริ่มพูด' จะทำหน้าที่สลับโหมด
if st.session_state.is_listening:
    # ใช้วิธี webrtc_streamer ในโหมด audio-only
    webrtc_ctx = webrtc_streamer(
        key="speech_input",
        mode=WebRtcMode.SENDONLY,
        audio_processor_factory=AudioProcessor,  # ใช้ AudioProcessor ที่เราสร้าง
        media_stream_constraints={"video": False, "audio": True},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    st.session_state.webrtc_state = webrtc_ctx
    st.info("⚠️ คลิกปุ่ม Start (สีเขียว) เพื่อเริ่มพูด เมื่อพูดเสร็จแล้วให้กด Stop (สีแดง)")

    # ตรวจสอบว่าผู้ใช้หยุด Stream หรือยัง
    if webrtc_ctx.state.playing == False and webrtc_ctx.audio_processor:
        audio_processor = webrtc_ctx.audio_processor

        # แปลง Audio Chunk ที่บันทึกไว้ให้เป็น Audio Data Format
        if audio_processor.audio_chunks:
            st.warning("กำลังประมวลผลเสียง... (อาจใช้เวลาสักครู่)")
            try:
                # รวม Audio Chunks เป็นไฟล์ WAV
                audio_data = audio_processor.recognizer.AudioData(
                    b"".join([chunk.to_bytes() for chunk in audio_processor.audio_chunks]),
                    sample_rate=audio_processor.recognizer.SAMPLE_RATE,
                    sample_width=audio_processor.recognizer.SAMPLE_WIDTH
                )
                # เรียกใช้ฟังก์ชันตรวจสอบคำศัพท์
                process_speech(audio_data)

            except Exception as e:
                st.session_state.result_text = f"❌ เกิดข้อผิดพลาดในการรวบรวมไฟล์เสียง: {e}"
                st.session_state.is_listening = False
                st.rerun()
        else:
            # กรณีผู้ใช้กด Stop ทันทีโดยไม่มีเสียง
            st.session_state.is_listening = False
            st.session_state.result_text = "❌ ไม่พบเสียงพูด"
            st.rerun()

else:
    # ปุ่ม 'เริ่มพูด' จะทำหน้าที่สลับโหมด (ย้ายไปอยู่ด้านบนแล้ว)
    pass
# -------------------------------------------------------------

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