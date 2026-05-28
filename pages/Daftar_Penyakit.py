import streamlit as st
from PIL import Image
import os

st.title("📋 Daftar Penyakit Kulit")

with open("penyakit.txt", "r", encoding="utf-8") as file:
    penyakit = file.read().split("\n")

for item in penyakit:

    st.subheader(item)

    image_path = f"img/{item}.jpg"

    if os.path.exists(image_path):
        img = Image.open(image_path)
        st.image(img, width=250)

    desc_path = f"Deskripsi_penyakit/{item}.txt"

    if os.path.exists(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            st.write(f.read())

    st.markdown("---")