import streamlit as st

st.title("🛡 Pencegahan Penyakit Kulit")

st.write("""
Berikut beberapa cara untuk mencegah penyakit kulit:
""")

tips = [
    "Menjaga kebersihan kulit setiap hari",
    "Mandi secara teratur menggunakan sabun",
    "Menghindari penggunaan barang pribadi secara bergantian",
    "Mengonsumsi makanan bergizi",
    "Memperbanyak minum air putih",
    "Menghindari garukan pada kulit yang gatal",
    "Menggunakan pelembap untuk kulit kering",
    "Menghindari paparan bahan kimia berbahaya",
    "Menggunakan pakaian yang bersih dan nyaman",
    "Segera memeriksakan diri ke dokter jika gejala semakin parah"
]

for tip in tips:
    st.success(tip)