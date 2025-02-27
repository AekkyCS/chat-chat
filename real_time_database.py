import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# โหลด Firebase Credentials
if not firebase_admin._apps:
    cred = credentials.Certificate("computer-science-34b7a-firebase-adminsdk-az6ze-0a7401a177.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://computer-science-34b7a-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

# อ้างอิงไปยัง Firebase Database
chat_ref = db.reference("/chat_messages")

# ตั้งค่า UI ของ Chat App
st.title("💬 Real-time Chat App")
username = st.text_input("👤 Your name", key="username")

# แสดงข้อความแชทแบบ Real-time
st.subheader("📢 Chat room")
def new_func(chat_ref):
    return chat_ref.get()

messages = new_func(chat_ref)

if messages:
    for key, msg in messages.items():
        st.write(f"**{msg['username']}**: {msg['message']}")

# ส่งข้อความ
message = st.text_input("💬 message...", key="message")

if st.button("🚀 send"):
    if username and message:
        chat_ref.push({
            "username": username,
            "message": message,
            "timestamp": time.time()
        })
        st.rerun()  # รีเฟรชหน้าจออัตโนมัติ
    else:
        st.warning("⚠️ Please fill in your name and message before sending!")

if username == "aekky":
    if st.button("🗑️ ล้างแชท"):
        chat_ref.set({})
        st.rerun()