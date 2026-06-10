import streamlit as str
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
str.set_page_config(page_title="Bajaj Semarang BOT", page_icon="🛺", layout="centered")

str.title("🛺 BoSem: Chatbot Bajaj Semarang")
str.caption("Monggo! Tanya rute, tarif, atau info seputar Bajaj di Semarang.")

# --- INITIALISASI GOOGLE GEMINI AI ---
try:
    # Mengambil API Key dari Streamlit Secrets
    api_key = str.secrets["ANTIGRAVITY_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    api_key = None

if "messages" not in str.session_state:
    str.session_state.messages = [
        {"role": "user", "parts": ["Kamu adalah BoSem, chatbot asisten layanan Bajaj di Kota Semarang. Jawablah dengan ramah, informatif, gunakan sedikit bahasa khas Semarangan (seperti 'Sih', 'Ik', 'Monggo', 'Lur'). Berikan estimasi rute atau tarif sekitar Lawang Sewu, Kota Lama, atau Simpang Lima."]},
        {"role": "model", "parts": ["Halo lur! Isok tak bantu opo iki seputar Bajaj Semarang? 🛺"]}
    ]

# Tampilkan riwayat
for msg in str.session_state.messages:
    # Jangan tampilkan prompt system pertama agar rapi
    if msg["parts"][0].startswith("Kamu adalah BoSem"):
        continue
    role = "user" if msg["role"] == "user" else "assistant"
    with str.chat_message(role):
        str.write(msg["parts"][0])

# Input pengguna
if user_input := str.chat_input("Mau pergi ke mana hari ini?"):
    with str.chat_message("user"):
        str.write(user_input)
    
    str.session_state.messages.append({"role": "user", "parts": [user_input]})
    
    with str.chat_message("assistant"):
        with str.spinner("Sik ya, lagi mikir..."):
            try:
                # Menggunakan model Gemini resmi yang stabil
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(str.session_state.messages)
                answer = response.text
                str.write(answer)
            except Exception as e:
                # Cadangan jika API Key belum dimasukkan di Secrets
                if "tarif" in user_input.lower() or "harga" in user_input.lower():
                    answer = "Tarif dasar Bajaj Semarang mulai dari Rp 10.000 untak jarak dekat lur. Kalau keliling kota bisa nego langsung sama pak sopirnya!"
                else:
                    answer = "Yoo lur, mau jalan-jalan ke Simpang Lima, Kota Lama, atau Lawang Sewu? Bajaj Semarang siap mengantar kamu kapan aja! 🛺"
                str.write(answer)
            
            str.session_state.messages.append({"role": "model", "parts": [answer]})
