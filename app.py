import streamlit as str

# --- KONFIGURASI HALAMAN ---
str.set_page_config(page_title="Bajaj Semarang BOT", page_icon="🛺", layout="centered")

# --- JUDUL & TAMPILAN ---
str.title("🛺 BoSem: Chatbot Bajaj Semarang")
str.caption("Monggo! Tanya rute, tarif, atau info seputar Bajaj di Semarang.")

# --- INISIALISASI RIWAYAT CHAT ---
if "messages" not in str.session_state:
    str.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Halo lur! Isok tak bantu opo iki seputar Bajaj Semarang? 🛺"
        }
    ]

# --- MENAMPILKAN RIWAYAT CHAT ---
for msg in str.session_state.messages:
    with str.chat_message(msg["role"]):
        str.write(msg["content"])

# --- INPUT DARI PENGGUNA ---
if user_input := str.chat_input("Mau pergi ke mana hari ini?"):
    # Tampilkan chat pengguna
    with str.chat_message("user"):
        str.write(user_input)
    
    # Simpan ke session state
    str.session_state.messages.append({"role": "user", "content": user_input})
    
    # --- PROSES JAWABAN INSTAN (ANTI MACET) ---
    with str.chat_message("assistant"):
        with str.spinner("Sik ya..."):
            teks_input = user_input.lower()
            
            # Logika pencarian kata kunci rute & tarif Semarang
            if "tarif" in teks_input or "harga" in teks_input or "ongkos" in teks_input:
                answer = "Tarif dasar Bajaj Semarang mulai dari Rp 10.000 untak jarak dekat lur. Kalau mau keliling seharian bisa nego langsung sama pak sopirnya, dijamin murah!"
            elif "rute" in teks_input or "jalan" in teks_input or "ke mana" in teks_input:
                answer = "BoSem siap anter kamu ke rute-rute andalan Semarang lur! Mulai dari Simpang Lima, Kota Lama, Lawang Sewu, Sampookong, sampe Klenteng Sam Poo Kong gass terus!"
            elif "kota lama" in teks_input:
                answer = "Yoo lur, kalau mau ke Kota Lama tarif bajajnya sekitar Rp 15.000 - Rp 25.000 aja dari Simpang Lima. Tempatnya asyik buat foto-foto!"
            elif "lawang sewu" in teks_input:
                answer = "Ke Lawang Sewu? Siap lur! Naik bajaj lewat jalan pemuda biar cepet, tarifnya aman dikantong mahasiswa."
            elif "halo" in teks_input or "hai" in teks_input or "p" == teks_input:
                answer = "Halo juga lur! Selamat datang di layanan Bajaj Semarang. Mau jalan-jalan ke mana kita hari ini? 🛺"
            else:
                answer = "Wah, BoSem agak kurang paham maksudmu lur hhehe. Tapi tenang, Bajaj Semarang siap mengantar kamu keliling Lawang Sewu, Kota Lama, atau Simpang Lima kapan aja! Mau tanya tarif atau rute?"

            str.write(answer)
            
            # Simpan jawaban ke session state
            str.session_state.messages.append({"role": "assistant", "content": answer})
