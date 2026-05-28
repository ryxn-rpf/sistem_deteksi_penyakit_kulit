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

# Root folder proyek Anda (/mount/src/sistem_deteksi_penyakit_kulit)
BASE_DIR = Path(__file__).resolve().parent.parent

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

    

    # 1. Cari folder data secara dinamis (mengatasi masalah huruf besar/kecil)
    def get_exact_folder_name(base_path, target_name):
        """Mencari folder tanpa memedulikan huruf besar/kecil"""
        if base_path.exists():
            for folder in base_path.iterdir():
                if folder.is_dir() and folder.name.lower() == target_name.lower():
                    return folder
        return base_path / target_name # fallback jika tidak ditemukan

    folder_gejala = get_exact_folder_name(BASE_DIR, "Gejala_penyakit")
    folder_deskripsi = get_exact_folder_name(BASE_DIR, "Deskripsi_penyakit")
    folder_obat = get_exact_folder_name(BASE_DIR, "Obat_penyakit")

    # 2. Cek file penyakit.txt
    penyakit_file = BASE_DIR / "penyakit.txt"
    if not penyakit_file.exists():
        st.error(f"❌ File tidak ditemukan: {penyakit_file}")
        return

    with open(penyakit_file, "r", encoding="utf-8") as f:
        diseases_list = [line.strip() for line in f.read().splitlines() if line.strip()]

    # 3. Looping untuk membaca semua file penyakit
    for disease in diseases_list:
        disease = disease.strip()

        # Cari file penyakit secara case-insensitive di dalam folder gejala
        gejala_path = None
        if folder_gejala.exists():
            for file_item in folder_gejala.glob("*.txt"):
                if file_item.stem.lower() == disease.lower():
                    gejala_path = file_item
                    break

        # Jika file tidak ditemukan lewat pencarian dinamis, gunakan path standar
        if not gejala_path:
            gejala_path = folder_gejala / f"{disease}.txt"

        if not gejala_path.exists():
            st.error(f"❌ File gejala tidak ditemukan untuk penyakit: {disease} di jalur {gejala_path}")
            continue

        # BACA GEJALA
        with open(gejala_path, "r", encoding="utf-8") as file:
            s_list = [line.strip() for line in file.read().splitlines()]
        
        diseases_symptoms.append(s_list)
        symptom_map[tuple(s_list)] = disease

        # BACA DESKRIPSI
        desc_path = folder_deskripsi / f"{gejala_path.stem}.txt"
        if desc_path.exists():
            with open(desc_path, "r", encoding="utf-8") as file:
                d_desc_map[disease] = file.read()
        else:
            # Coba cari secara case-insensitive jika tidak langsung ketemu
            found_desc = False
            if folder_deskripsi.exists():
                for f_item in folder_deskripsi.glob("*.txt"):
                    if f_item.stem.lower() == disease.lower():
                        with open(f_item, "r", encoding="utf-8") as file:
                            d_desc_map[disease] = file.read()
                        found_desc = True
                        break
            if not found_desc:
                d_desc_map[disease] = "Deskripsi tidak tersedia."

        # BACA OBAT
        treatment_path = folder_obat / f"{gejala_path.stem}.txt"
        if treatment_path.exists():
            with open(treatment_path, "r", encoding="utf-8") as file:
                d_treatment_map[disease] = file.read()
        else:
            # Coba cari secara case-insensitive jika tidak langsung ketemu
            found_treat = False
            if folder_obat.exists():
                for f_item in folder_obat.glob("*.txt"):
                    if f_item.stem.lower() == disease.lower():
                        with open(f_item, "r", encoding="utf-8") as file:
                            d_treatment_map[disease] = file.read()
                        found_treat = True
                        break
            if not found_treat:
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

        # KONDISI BARU: Jika max_disease tetap kosong (artinya user pilih 'tidak' semua)
        if max_disease == "" or max_count == 0:
            st.warning("⚠ Anda tidak memilih gejala apa pun atau tidak ada gejala 'Ya' yang cocok dengan penyakit mana pun.")
            st.info("Silakan pilih setidaknya satu gejala yang sesuai dengan kondisi Anda.")
        
        else:
            # Jalankan ini HANYA JIKA max_disease ada isinya
            st.warning("⚠ Penyakit tidak cocok secara pasti")
            st.info(f"Kemungkinan mendekati: {max_disease} (Kecocokan: {max_count} gejala)")

            image_path = BASE_DIR / "img" / f"{max_disease}.jpg"

            if image_path.exists():
                st.image(Image.open(image_path), caption=max_disease, width=300)

            st.subheader("📖 Deskripsi Penyakit")
            # Menggunakan .get() lebih aman daripada [] untuk menghindari KeyError
            st.write(d_desc_map.get(max_disease, "Deskripsi tidak tersedia."))

            st.subheader("💊 Pengobatan")
            st.write(d_treatment_map.get(max_disease, "Informasi pengobatan tidak tersedia."))
