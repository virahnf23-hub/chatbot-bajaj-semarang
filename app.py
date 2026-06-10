import streamlit as str

# --- KONFIGURASI HALAMAN ---
str.set_page_config(page_title="BoSem: Bajaj Semarang", page_icon="🛺", layout="centered")

# --- JUDUL & TAMPILAN UTAMA ---
str.title("🛺 BoSem: Chatbot Bajaj Semarang")
str.caption("Monggo lur! Tanya rute, tarif, lokasi wisata, sampai rekomendasi kulineran di Semarang.")

# --- SIDEBAR INTERAKTIF (FITUR TAMBAHAN) ---
with str.sidebar:
    str.header("🛺 Menu Cepat BoSem")
    str.write("Males ngetik? Klik tombol di bawah ini buat info instan:")
    
    # Tombol otomatis yang akan mengisi chat_input secara tidak langsung
    btn_tarif = str.button("💰 Cek Tarif Dasar")
    btn_kuliner = str.button("🧆 Rekomendasi Kuliner")
    btn_wisata = str.button("🏛️ Rute Wisata Hits")
    
    str.markdown("---")
    str.markdown("**Status Armada:** ✅ Siap Gass\n\n**Wilayah Operasional:** Kota Semarang & sekitarnya.")

# --- INISIALISASI RIWAYAT CHAT ---
if "messages" not in str.session_state:
    str.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Halo lur! Isok tak bantu opo iki seputar Bajaj Semarang? Mau nanya rute, tarif, atau kulineran sing maknyus? 🛺"
        }
    ]

# --- MENANGKAP AKSI DARI BUTTON SIDEBAR ---
# Trik agar ketika tombol diklik, langsung memicu respons chatbot
sidebar_input = None
if btn_tarif:
    sidebar_input = "tarif"
elif btn_kuliner:
    sidebar_input = "kuliner"
elif btn_wisata:
    sidebar_input = "rute"

# --- INPUT UTAMA (DARI USER CHAT ATAU SIDEBAR) ---
user_input = str.chat_input("Mau pergi ke mana hari ini?")

# Jika tombol sidebar diklik, override user_input
if sidebar_input:
    user_input = sidebar_input

# --- PROSES CHAT ---
# Menampilkan riwayat chat yang sudah ada
for msg in str.session_state.messages:
    with str.chat_message(msg["role"]):
        str.write(msg["content"])

# Jika ada input baru masuk
if user_input:
    # Jika input berasal dari tombol sidebar, tampilkan teks rapi di sisi user
    display_user_text = user_input
    if user_input == "tarif": display_user_text = "Berapa tarif dasar bajajnya, Lur?"
    elif user_input == "kuliner": display_user_text = "Minta rekomendasi kuliner Semarang dong!"
    elif user_input == "rute": display_user_text = "Rute wisata hits di Semarang ke mana aja?"

    with str.chat_message("user"):
        str.write(display_user_text)
    
    str.session_state.messages.append({"role": "user", "content": display_user_text})
    
    # Respons logika asisten
    with str.chat_message("assistant"):
        with str.spinner("Sik..."):
            teks_input = user_input.lower()
            
            if "tarif" in teks_input or "harga" in teks_input or "ongkos" in teks_input:
                answer = "Tarif dasar Bajaj Semarang mulai dari **Rp 10.000** untuk jarak dekat (sekitaran 1-2 KM) lur. Kalau mau sewa keliling seharian bisa nego langsung sama pak sopirnya, dijamin luwih murah dan gass terus!"
            
            elif "rute" in teks_input or "wisata" in teks_input or "jalan" in teks_input:
                answer = "BoSem siap ngater kamu ke rute-rute andalan Semarang lur! Mulai dari pesona **Kota Lama**, mistisnya **Lawang Sewu**, megahnya **Sampookong**, sampai nyari takjil/jajanan di **Simpang Lima**!"
            
            elif "kuliner" in teks_input or "makan" in teks_input or "lumpia" in teks_input:
                answer = "Wah kalau kuliner Semarang juarane lur! Naik bajaj tak anter ke Lumpia Gang Lombok, Tahu Gimbal Pak H. Edy, sego kucing di Angkringan Pandanaran, atau hunting Wingko Babat mumpung anget!"
            
            elif "kota lama" in teks_input:
                answer = "Yoo lur, kalau mau ke Kota Lama tarif bajajnya sekitar Rp 15.000 - Rp 25.000 aja dari Simpang Lima. Tempatnya asyik pol buat foto-foto estetik!"
                
            elif "lawang sewu" in teks_input:
                answer = "Ke Lawang Sewu? Siap lur! Tak anter lewat jalan Pemuda biar cepet, tarifnya aman dikantong mahasiswa. Berani uji nyali bengi-bengi gak, ik? hhehe."
                
            elif "halo" in teks_input or "hai" in teks_input or "p" == teks_input:
                answer = "Halo juga lur! Selamat datang di layanan BoSem. Mau jalan-jalan atau kulineran ke mana kita hari ini? 🛺"
                
            else:
                answer = "Wah, BoSem agak kurang paham maksudmu lur hhehe. Tapi tenang, Bajaj Semarang siap mengantar kamu keliling Lawang Sewu, Kota Lama, Simpang Lima, atau berburu Lumpia! Coba klik menu di sebelah kiri aja lur!"

            str.write(answer)
            str.session_state.messages.append({"role": "assistant", "content": answer})
