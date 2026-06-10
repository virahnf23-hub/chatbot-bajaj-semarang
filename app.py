import streamlit as str
import openai  # Atau library AI sesuai dokumentasi resmi "Antigravity AI" yang kamu gunakan

# --- KONFIGURASI HALAMAN ---
str.set_page_config(page_title="Bajaj Semarang BOT", page_icon="🛺", layout="centered")

# --- JUDUL & TAMPILAN ---
str.title("🛺 BoSem: Chatbot Bajaj Semarang")
str.caption("Monggo! Tanya rute, tarif, atau info seputar Bajaj di Semarang (Simpang Lima, Kota Lama, Sampookong, dll).")

# --- INISIALISASI API KEY & SESSION STATE ---
# Mengambil API Key dari Streamlit Secrets (untuk keamanan saat deploy)
try:
    api_key = str.secrets["ANTIGRAVITY_API_KEY"]
except KeyError:
    api_key = "KODE_API_KEY_MOCKUP_KAMU"  # Gantilah jika testing lokal

# Inisialisasi riwayat obrolan jika belum ada
if "messages" not in str.session_state:
    str.session_state.messages = [
        {
            "role": "system", 
            "content": "Kamu adalah BoSem, chatbot asisten untuk layanan Bajaj di Kota Semarang. Jawablah dengan ramah, informatif, kadang gunakan sedikit bahasa khas Semarangan (seperti 'Sih', 'Ik', 'Monggo'). Berikan estimasi rute atau tarif yang logis jika ditanya tentang tempat wisata seperti Lawang Sewu, Kota Lama, atau Simpang Lima."
        },
        {
            "role": "assistant", 
            "content": "Halo lur! Isok tak bantu opo iki seputar Bajaj Semarang? 🛺"
        }
    ]

# --- MENAMPILKAN RIWAYAT CHAT ---
for msg in str.session_state.messages:
    if msg["role"] != "system":
        with str.chat_message(msg["role"]):
            str.write(msg["content"])

# --- INPUT DARI PENGGUNA ---
if user_input := str.chat_input("Mau pergi ke mana hari ini?"):
    # Tampilkan chat pengguna
    with str.chat_message("user"):
        str.write(user_input)
    
    # Simpan ke session state
    str.session_state.messages.append({"role": "user", "content": user_input})
    
    # --- PROSES MEMANGGIL AI (ANTIGRAVITY / OPENAI COMPATIBLE) ---
    with str.chat_message("assistant"):
        with str.spinner("Sik ya, lagi mikir..."):
            try:
                # Catatan: Sesuaikan endpoint/client jika Antigravity menggunakan SDK khusus.
                # Format di bawah ini menggunakan standar OpenAI client yang umum dipakai banyak provider AI.
                client = openai.OpenAI(api_key=api_key, base_url="https://api.antigravity.ai/v1") # Sesuaikan URL base jika ada
                
                response = client.chat.completions.create(
                    model="antigravity-model-name", # Ganti dengan nama model Antigravity-mu
                    messages=str.session_state.messages
                )
                
                answer = response.choices[0].message.content
                str.write(answer)
                
            except Exception as e:
                # Fallback / Mockup jika API belum terhubung sempurna agar chatbot tetap bisa demo
                if "Kota Lama" in user_input or "kota lama" in user_input:
                    answer = "Yoo lur, kalau dari Simpang Lima ke Kota Lama tarif bajajnya sekitar Rp 15.000 - Rp 25.000, tergantung pinter-pinteranmu nawar sih hhehe. Mau langsung gass?"
                elif "tarif" in user_input.lower() or "harga" in user_input.lower():
                    answer = "Tarif dasar Bajaj Semarang mulai dari Rp 10.000 untak jarak dekat lur. Kalau keliling kota bisa nego langsung sama pak sopirnya!"
                else:
                    answer = f"Waduh koneksiku rada ngadat lur (Error: {e}). Tapi tenang, Bajaj Semarang siap mengantar kamu keliling Lawang Sewu atau Simpang Lima kapan aja!"
                
                str.write(answer)
            
            # Simpan jawaban asisten ke session state
            str.session_state.messages.append({"role": "assistant", "content": answer})
