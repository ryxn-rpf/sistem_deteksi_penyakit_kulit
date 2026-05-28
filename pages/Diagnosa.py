import collections
import collections.abc

collections.Mapping = collections.abc.Mapping
collections.Sequence = collections.abc.Sequence
collections.Iterable = collections.abc.Iterable
collections.Callable = collections.abc.Callable

import streamlit as st
from experta import *
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

    with open("penyakit.txt", "r", encoding="utf-8") as diseases:
        diseases_t = diseases.read()
        diseases_list = diseases_t.split("\n")

    for disease in diseases_list:

        with open(f"Gejala_penyakit/{disease}.txt", "r", encoding="utf-8") as file:
            s_list = file.read().split("\n")
            diseases_symptoms.append(s_list)
            symptom_map[str(s_list)] = disease

        with open(f"Deskripsi_penyakit/{disease}.txt", "r", encoding="utf-8") as file:
            d_desc_map[disease] = file.read()

        with open(f"Obat_penyakit/{disease}.txt", "r", encoding="utf-8") as file:
            d_treatment_map[disease] = file.read()

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
    "kulit_membengkak",
    "benjolan_di_kulit",
    "mengeluarkan_nanah",
    "demam",
    "mata_merah",
    "kulit_kepala_berminyak",
    "rasa_gatal",
    "luka_dari_bagian_mulut",
    "memiliki_gelembung_berisi_air",
    "rasa_nyeri",
    "kulit_melepuh",
    "memiliki_bercak_bercak_merah",
    "iritasi_kulit",
    "uban_muncul_sebelum_waktunya",
    "muncul_keringat_berlebihan",
    "menimbulkan_warna_kekuningan",
    "kulit_kering",
    "kulit_bersisik",
    "bintik_atau_bintik_merah",
    "ruam_kulit",
    "luka",
    "mati_rasa",
    "luka_tidak_terasa_nyeri",
    "kulit_tidak_berkeringat",
    "kesemutan",
    "benjolan_berwarna_merah_atau_kulit_kemerahan",
    "infeksi_kulit",
    "sakit_kepala",
    "rasa_kelelahan",
    "mual",
    "nyeri_otot",
    "benjolan_putih",
    "bintil",
    "lesi_gatal_atau_kemerahan",
    "tonjolan_kasar_atau_keras",
    "bintik_atau_bercak_putih_berwarna_terang",
    "ruam_berbentuk_cincin"
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
# PROSES DIAGNOSA
# =========================================

if st.button("Diagnosa Penyakit"):

    found = False

    for key, disease in symptom_map.items():

        temp_list = eval(key)

        if temp_list == user_answers:

            found = True

            st.success(f"✅ Kemungkinan penyakit: {disease}")

            image_path = f"./img/{disease}.jpg"

            if os.path.exists(image_path):
                img = Image.open(image_path)
                st.image(img, caption=disease, width=300)

            st.subheader("📖 Deskripsi Penyakit")
            st.write(d_desc_map[disease])

            st.subheader("💊 Pengobatan")
            st.write(d_treatment_map[disease])

            break

    if not found:

        max_count = 0
        max_disease = ""

        for key, val in symptom_map.items():

            count = 0
            temp_list = eval(key)

            for j in range(len(user_answers)):
                if temp_list[j] == user_answers[j] and user_answers[j] == "ya":
                    count += 1

            if count > max_count:
                max_count = count
                max_disease = val

        st.warning("⚠ Penyakit tidak cocok secara pasti")

        st.info(f"Kemungkinan mendekati: {max_disease}")

        image_path = f"./img/{max_disease}.jpg"

        if os.path.exists(image_path):
            img = Image.open(image_path)
            st.image(img, caption=max_disease, width=300)

        st.subheader("📖 Deskripsi Penyakit")
        st.write(d_desc_map[max_disease])

        st.subheader("💊 Pengobatan")
        st.write(d_treatment_map[max_disease])