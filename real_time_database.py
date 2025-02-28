import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import json
import os


firebase_credentials ={
  "type": "service_account",
  "project_id": "computer-science-34b7a",
  "private_key_id": "52c82f81f80f7ebb4fffddcad6e12f5315f3a9ce",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQC83oAdtf0goaCD\ne4IN5xiE70kaLHuD9cT8o8IuW66yUsTCCSrGRvpOZMMkSe39swd6gVbnKI7nJ+R3\nPj7F/sc7F+zYN6grVzzJeDWlPnD88kVOm85Y8ShLKBF9BKy3Mbtx+9NBZa6pA2g8\ngio/XTy2bD6094syFrBR3/NRqAacD/Y3R2aZfQmqxMRqAzXfw5NMAnya9dwccRsm\nRjujXF9LdtLgGHTywqYRz+a7CJj8yGQokpaJKzdEm0Q4fQnnzWbEFKVeX7jgg+71\nUNzKv31XI9VQmF7asngcP2JMinwXehBNSNMlGbCvU6E1Tt+yQA0cvqdQNkHayuJd\nb0jEiv4vAgMBAAECgf95DaccYXEvnRaIvRvMgtTAx+Xf82wq4VViAz9kzif/APKI\n9Ayke4U48vZ53UclbpPrbpAKSXwQQbHcxcuvY/MDySZsDiTuc07z3J/hn4Ed4hGn\n1Z2aX0Hnyaenh1PGYcQOh5GCjnbGZg3wxGGzHW8ppQDHwRYKX1iwFRwjoWL5lBvJ\nD/yIhmEH8RI90z8vIvdpCZWOFV0kblUxesM/+lSV0hurKopzDJIu2QmqciS8SxtF\n4kCVJCNMJMyMLSWA7rnWekQTCIpG0oVEj7IOXevoWsch1eZUe5nQmGZGtQQqxAIk\n1EJb+XfQoDPn9Mqs9v3ACgNUopNKNveWbcs9/FUCgYEA9rl8wZHgmR2Qn81pdhqA\nAWjZ2e034761KVp21voAnjInuEkAB1887rOB6QZOaIL8qA2Hzvz7UFPNnqvl+pDj\n8HBxhCpTMk+XijcGhHJdIrsqYdZXXHWmlv7PE3AqxIKZxzJHzTfgIL7S880BKSYU\n3bfRjpIGxRNR7q+KEFmH1nsCgYEAw/g0Sm1ap5QSk19BfOFBsvMFCEXCFKCkgTkc\nnZdhudAdhwpCCX2fZ6IpyuM9jttgPLfCBFtKaiU8d3W5u5DVdS95IWrqbosSRpCw\nnhNCfu3Dn3a4ypNQ3OLvoQgqYYVEGz5mUGiCVcqIc2F3ZLB2mBOLYO9AgDicYdhE\nHWaXot0CgYAPrBqrpRuSPlmIfSDc2rQU4tcry7DIK74QQWnZIApYAjGZuDFjRn51\nXzu6VKc4ZlGsTye4U0OXh6tBEARM1VVVWZ8sWQ/t2zZyFiq40RbvdNotWtMz0Vli\nsA7xWietUep4x83d0FXRXq3BxNz1AzFCIEIUf1wkuqRyt/3aKgXB7wKBgBfTdYgX\nA46cUiXYzv1/5Zz8LwByesZHQbj0WKZQYXFV/EEO3jiJLXhMHwir2DAmO+0l6lDd\nSI7fOBrOFWbYlRtKSk/lz9rgzbgGn3KYpN0Jy1738D+w6YPxk3DgrUZuDXnCfG4K\nRs5ncW+Vyg5T5hdXSPrgG9d7Coha4u0wK/+BAoGAIgJ27/FhkrTJWqYNjq9m5s57\nOArgSYKbUHv+UOWhyjICp6zJ4zaQjubKVScu7FKyVbJfThfTtueDZNWHR0jByIF9\nyGjG5AU/0kKTcfsu7o0zqWIeOhhbYKOn4iDn0dvNrun9Bhtm5mdB+MmwKeAbTJzv\nWrCSyEl13RvgJE+yoBY=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-az6ze@computer-science-34b7a.iam.gserviceaccount.com",
  "client_id": "102185166294179839636",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-az6ze%40computer-science-34b7a.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# โหลด Firebase Credentials
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://computer-science-34b7a-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

# ตั้งค่า UI ของ Chat App
st.title("💬 CS Chat Room")
username = st.text_input("👤 Your name", key="username")

# ดึงข้อมูลแชทจาก Firebase
def get_messages():
    chat_ref = db.reference("/chat_messages")
    return chat_ref.get()

st.subheader("📢 Chat room")
chat_box = st.empty()  # สร้างกล่องแสดงข้อความ

# โหลดข้อความใหม่ทุก ๆ 1 วินาที
if "last_refresh" not in st.session_state or time.time() - st.session_state["last_refresh"] > 1:
    st.session_state["last_refresh"] = time.time()
    messages = get_messages()
    with chat_box.container():
        if messages:
            for key, msg in messages.items():
                if msg["username"] == username:
                    # จัดสไตล์ข้อความของผู้ใช้เองให้อยู่ด้านขวาและเป็นสีแดง
                    st.markdown(f'<div style="text-align: right; color: red;"> <b>{msg["username"]}</b>: {msg["message"]} </div>', unsafe_allow_html=True)
                else:
                    # ข้อความของคนอื่นแสดงตามปกติ
                    st.write(f"**{msg['username']}**: {msg['message']}")
    st.experimental_rerun()

# ส่งข้อความ
message = st.text_input("💬 message...", key="message")

if st.button("🚀 send"):
    if username and message:
        chat_ref = db.reference("/chat_messages")
        chat_ref.push({
            "username": username,
            "message": message,
            "timestamp": time.time()
        })
        st.experimental_rerun()
    else:
        st.warning("⚠️ Please fill in your name and message before sending!")

# ปุ่มล้างแชท (เฉพาะ user 'aekky')
if username == "aekky":
    if st.button("🗑️ ล้างแชท"):
        chat_ref = db.reference("/chat_messages")
        chat_ref.set({})
        st.experimental_rerun()
