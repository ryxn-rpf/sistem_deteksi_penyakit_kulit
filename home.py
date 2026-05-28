import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Sistem Pakar Deteksi Penyakit Kulit")

st.write("""
Selamat datang di aplikasi sistem pakar deteksi penyakit kulit.

Gunakan menu sidebar untuk:
- Diagnosa penyakit
- Melihat data penyakit
- Galeri gambar penyakit
- Deteksi gambar kulit
- Bantuan penggunaan
""")