from pathlib import Path
import collections
import collections.abc

collections.Mapping = collections.abc.Mapping
collections.Sequence = collections.abc.Sequence
collections.Iterable = collections.abc.Iterable
collections.Callable = collections.abc.Callable

import streamlit as st
from PIL import Image
import os

# =========================================
# DATA GLOBAL
# =========================================

diseases_list = []
diseases_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}

# =========================================
# PREPROCESS DATA
# =========================================

def preprocess():
    global diseases_list, diseases_symptoms
    global symptom_map, d_desc_map, d_treatment_map

    diseases_symptoms = []
    symptom_map = {}
    d_desc_map = {}
    d_treatment_map = {}

    BASE_DIR = Path(__file__).resolve().parent.parent

    # 1. Pastikan file utama ada
    penyakit_file = BASE_DIR / "penyakit.txt"
    if not penyakit_file.exists():
        st.error(f"File tidak ditemukan: {penyakit_file}")
        return

    with open(penyakit_file, "r", encoding="utf-8") as f:
        diseases_list = [line.strip() for line in f.read().splitlines() if line.strip()]

    for disease in diseases_list:
        # Menghapus spasi liar di nama penyakit
        disease = disease.strip()

        # 2. Jalur Folder (Pastikan huruf besar/kecil di folder GitHub Anda SAMA PERSIS!)
        gejala_path = BASE_DIR / "Gejala_penyakit" / f"{disease}.txt"
        desc_path = BASE_DIR / "Deskripsi_penyakit" / f"{disease}.txt"
        treatment_path = BASE_DIR / "Obat_penyakit" / f"{disease}.txt"

        # Cek apakah file-file tersebut benar-benar ada sebelum dibuka
        if not gejala_path.exists():
            st.error(f"File gejala tidak ditemukan untuk penyakit: {disease} di jalur {gejala_path}")
            continue

        # BACA GEJALA
        with open(gejala_path, "r", encoding="utf-8") as file:
            s_list = [line.strip() for line in file.read().splitlines()]
        
        diseases_symptoms.append(s_list)
        
        # CATATAN: Pastikan isi file txt gejala Anda adalah susunan "ya"/"tidak" 
        # sebanyak 37 baris yang urutannya sama dengan list 'symptoms' di Streamlit.
        symptom_map[tuple(s_list)] = disease

        # BACA DESKRIPSI
        if desc_path.exists():
            with open(desc_path, "r", encoding="utf-8") as file:
                d_desc_map[disease] = file.read()
        else:
            d_desc_map[disease] = "Deskripsi tidak tersedia."

        # BACA OBAT
        if treatment_path.exists():
            with open(treatment_path, "r", encoding="utf-8") as file:
                d_treatment_map[disease] = file.read()
        else:
            d_treatment_map[disease] = "Informasi pengobatan tidak tersedia."

# =========================================
# STREAMLIT UI
# =========================================

st.set_page_config(page_title="Deteksi Penyakit Kulit", layout="wide")

st.title("🩺 Sistem Cerdas Deteksi Penyakit Kulit")
st.write("Deteksi penyakit kulit berbasis sistem pakar menggunakan Experta dan Streamlit")

preprocess()

# =========================================
# LIST GEJALA
# =========================================

symptoms = [
    "kulit_membengkak","benjolan_di_kulit","mengeluarkan_nanah","demam",
    "mata_merah","kulit_kepala_berminyak","rasa_gatal","luka_dari_bagian_mulut",
    "memiliki_gelembung_berisi_air","rasa_nyeri","kulit_melepuh",
    "memiliki_bercak_bercak_merah","iritasi_kulit","uban_muncul_sebelum_waktunya",
    "muncul_keringat_berlebihan","menimbulkan_warna_kekuningan","kulit_kering",
    "kulit_bersisik","bintik_atau_bintik_merah","ruam_kulit","luka","mati_rasa",
    "luka_tidak_terasa_nyeri","kulit_tidak_berkeringat","kesemutan",
    "benjolan_berwarna_merah_atau_kulit_kemerahan","infeksi_kulit","sakit_kepala",
    "rasa_kelelahan","mual","nyeri_otot","benjolan_putih","bintil",
    "lesi_gatal_atau_kemerahan","tonjolan_kasar_atau_keras",
    "bintik_atau_bercak_putih_berwarna_terang","ruam_berbentuk_cincin"
]

# =========================================
# INPUT USER
# =========================================

user_answers = []

st.subheader("Pilih gejala yang dialami")

for i, symptom in enumerate(symptoms, start=1):

    nama_gejala = symptom.replace("_", " ").title()

    answer = st.selectbox(
        f"{i}. Apakah Anda mengalami {nama_gejala}?",
        ["tidak", "ya"],
        key=symptom
    )

    user_answers.append(answer)

# =========================================
# DIAGNOSA
# =========================================

if st.button("Diagnosa Penyakit"):

    found = False

    user_tuple = tuple(user_answers)

    # ======================
    # COCOK PERSIS
    # ======================
    for key, disease in symptom_map.items():

        if key == user_tuple:

            found = True
            st.success(f"✅ Kemungkinan penyakit: {disease}")

            image_path = BASE_DIR / "img" / f"{disease}.jpg"

            if image_path.exists():
                st.image(Image.open(image_path), caption=disease, width=300)

            st.subheader("📖 Deskripsi Penyakit")
            st.write(d_desc_map[disease])

            st.subheader("💊 Pengobatan")
            st.write(d_treatment_map[disease])

            break

    # ======================
    # TIDAK COCOK (fallback)
    # ======================
    if not found:

        max_count = 0
        max_disease = ""

        for key, val in symptom_map.items():

            count = 0

            for j in range(len(user_answers)):
                if key[j] == user_answers[j] and user_answers[j] == "ya":
                    count += 1

            if count > max_count:
                max_count = count
                max_disease = val

        st.warning("⚠ Penyakit tidak cocok secara pasti")
        st.info(f"Kemungkinan mendekati: {max_disease}")

        image_path = BASE_DIR / "img" / f"{max_disease}.jpg"

        if image_path.exists():
            st.image(Image.open(image_path), caption=max_disease, width=300)

        st.subheader("📖 Deskripsi Penyakit")
        st.write(d_desc_map[max_disease])

        st.subheader("💊 Pengobatan")
        st.write(d_treatment_map[max_disease])
