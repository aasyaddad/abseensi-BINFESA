import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Konfigurasi Halaman & Tema Tampilan Menarik
st.set_page_config(
    page_title="Sistem Absensi Kelas INF26B",
    page_icon="🎓",
    layout="wide"
)

# Kustomisasi Tampilan CSS agar lebih modern & berwarna
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #182848 0%, #4b6cb7 100%);
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #1e3d59;
    }
    </style>
""", unsafe_allow_html=True)

# File Penyimpanan Data CSV
DATA_SISWA_FILE = "data_siswa_inf26b.csv"
DATA_ABSENSI_FILE = "data_absensi_matkul_inf26b.csv"

# Inisialisasi Data Mahasiswa Default (Kelas INF26B Sesuai Gambar)
if not os.path.exists(DATA_SISWA_FILE):
    df_default_siswa = pd.DataFrame({
        "NPM": [
            "26051204004", "26051204005", "26051204006", "26051204030", "26051204031", 
            "26051204047", "26051204048", "26051204049", "26051204050", "26051204051", 
            "26051204052", "26051204061", "26051204062", "26051204063", "26051204064", 
            "26051204065", "26051204066", "26051204067", "26051204068", "26051204123", 
            "26051204171", "26051204172", "26051204178", "26051204179", "26051204180", 
            "26051204198", "26051204209", "26051204210", "26051204211", "26051204212", 
            "26051204213", "26051204222", "26051204223", "26051204224", "26051204225", 
            "26051204272", "26051204273", "26051204274", "26051204278"
        ],
        "Nama": [
            "HARDIANSYAH PUTRA", "MELYNDA APRILYA", "JOYCE VICTORYA DARENPUTRI", "ADINALDO AUREL FAJAR CRISTIAN", "JOVAN RAFAEL SUSANTO", 
            "ATIKA NOVA PUTRI ROHMATILLAH AR.", "PUAN AZIZA KHIRANI", "KORNELIUS YOSIA GUNAWAN", "AHMAD ASYADDAD", "TEGUH SOPHIAN", 
            "AQILAZKA DIFA PUTRA AL KAYYIS", "CHEN MASYHUD ALHAQ", "ADRIAN MAULANA RAMADHAN", "EVANT ALFARIO ANGGARA", "ZACKY RAYA RAMADHAN", 
            "MUAMMAR ZAKI ALFARUQ", "SATRIA NADIF ATHALLAH PRAWIRA", "ABDILLAH SALMAN", "MUHAMMAD DZIKRI ARSYAD", "RIHAN AFRIZAL", 
            "ALFREDO KAKA SIMANJUNTAK", "AFAFA GHINA HILYATI", "ANDIKA WAHYU PAMUNGKAS", "AHMAD THORIQUL ISLAM AL ILHAMI", "OKEU RIZKA ABDULHAKIM", 
            "ANDREA FABEAN DAFFA", "FIDIAH KURNIHAYATI", "ROZAK RIZKIA SAPUTRA", "RITHZY ERIXA CHRISSEMBER", "JAHSY AIZWAR RAKHMAN", 
            "FARAH NAYSHITA LATIF", "MUHAMMAD RASYA AL FIKRI", "ANRICO ALDEN PUTRA", "FAHLEN WIAN DENATA", "A GHIYATS KAUTSAR RAHMAN", 
            "DAFA WARDHANA AYANKUSYAH GARUSU", "LALU ANDIRA ATHALLAH WIRAYUDHIA", "MUKHAMAD RIZKY ALIFI", "RUTH LAMTIAR SIREGAR"
        ],
        "Kelas": ["INF26B"] * 39
    })
    df_default_siswa.to_csv(DATA_SISWA_FILE, index=False)

if not os.path.exists(DATA_ABSENSI_FILE):
    df_default_absen = pd.DataFrame(columns=["Tanggal", "Hari", "Mata Kuliah", "NPM", "Nama", "Kelas", "Status"])
    df_default_absen.to_csv(DATA_ABSENSI_FILE, index=False)

# Daftar Jadwal Mata Kuliah Berdasarkan Hari
JADWAL_KULIAH = {
    "Senin": ["Etika Profesi", "Pemrograman Dasar"],
    "Rabu": ["Interaksi Manusia dan Komputer"],
    "Kamis": ["Arsitektur dan Organisasi Komputer", "Aljabar Linier dan Matriks"],
    "Jum'at": ["Matematika"]
}

# --- HEADER UTAMA ---
st.title("🎓 Sistem Presensi Kuliah INF26B")
st.markdown("Aplikasi pencatatan kehadiran mahasiswa secara digital, real-time, dan terstruktur per mata kuliah.")
st.markdown("---")

# --- SIDEBAR NAVIGASI MENARIK ---
st.sidebar.markdown("### 📌 Menu Navigasi")
menu = st.sidebar.radio("Pilih Menu Utama", ["📝 Catat Kehadiran", "👥 Kelola Mahasiswa", "📊 Rekap & Statistik"])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tips:** Pastikan tanggal dan mata kuliah yang dipilih sudah sesuai dengan jadwal hari perkuliahan.")

# ==================== MENU 1: CATAT ABSEN ====================
if menu == "📝 Catat Kehadiran":
    st.header("📝 Formulir Absensi Mahasiswa")
    
    df_siswa = pd.read_csv(DATA_SISWA_FILE)
    
    if df_siswa.empty:
        st.warning("⚠️ Belum ada data mahasiswa. Silakan tambahkan melalui menu 'Kelola Mahasiswa'.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            tanggal_pilih = st.date_input("📅 Pilih Tanggal Absensi", datetime.today())
            nama_hari = tanggal_pilih.strftime('%A')
            mapping_hari = {"Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis", "Friday": "Jum'at", "Saturday": "Sabtu", "Sunday": "Minggu"}
            hari_indo = mapping_hari.get(nama_hari, "Senin")
            st.markdown(f"🗓️ Hari terdeteksi: **{hari_indo}**")
            
        with col2:
            list_matkul_hari_ini = JADWAL_KULIAH.get(hari_indo, ["Tidak ada jadwal kuliah rutin"])
            matkul_pilih = st.selectbox("📚 Pilih Mata Kuliah", list_matkul_hari_ini)
        
        siswa_kelas = df_siswa[df_siswa["Kelas"] == "INF26B"]
        
        st.markdown(f"### 📋 Daftar Mahasiswa INF26B — **{matkul_pilih}**")
        st.caption("Silakan ubah status kehadiran masing-masing mahasiswa di bawah ini:")
        
        with st.form("form_absensi"):
            status_kehadiran = {}
            for index, row in siswa_kelas.iterrows():
                cols = st.columns([3, 2])
                cols[0].markdown(f"👤 **{row['NPM']}** — {row['Nama']}")
                status_kehadiran[row['NPM']] = cols[1].selectbox(
                    f"Status {row['Nama']}", 
                    ["Hadir", "Izin", "Sakit", "Alpha"], 
                    key=f"status_{row['NPM']}",
                    label_visibility="collapsed"
                )
            
            st.markdown("")
            submitted = st.form_submit_button("💾 Simpan Data Presensi")
            
            if submitted:
                if "Tidak ada" in matkul_pilih:
                    st.error("❌ Tidak ada jadwal mata kuliah pada hari tersebut!")
                else:
                    df_absen = pd.read_csv(DATA_ABSENSI_FILE)
                    
                    df_absen = df_absen[~((df_absen["Tanggal"] == str(tanggal_pilih)) & (df_absen["Mata Kuliah"] == matkul_pilih) & (df_absen["Kelas"] == "INF26B"))]
                    
                    data_baru = []
                    for index, row in siswa_kelas.iterrows():
                        data_baru.append({
                            "Tanggal": str(tanggal_pilih),
                            "Hari": hari_indo,
                            "Mata Kuliah": matkul_pilih,
                            "NPM": row["NPM"],
                            "Nama": row["Nama"],
                            "Kelas": "INF26B",
                            "Status": status_kehadiran[row["NPM"]]
                        })
                    
                    df_baru_to_append = pd.DataFrame(data_baru)
                    df_absen = pd.concat([df_absen, df_baru_to_append], ignore_index=True)
                    df_absen.to_csv(DATA_ABSENSI_FILE, index=False)
                    
                    st.success(f"✅ Presensi mata kuliah **{matkul_pilih}** tanggal {tanggal_pilih} berhasil disimpan!")

# ==================== MENU 2: KELOLA MAHASISWA ====================
elif menu == "👥 Kelola Mahasiswa":
    st.header("👥 Manajemen Data Mahasiswa INF26B")
    
    df_siswa = pd.read_csv(DATA_SISWA_FILE)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("➕ Tambah Mahasiswa Baru")
        with st.form("form_tambah_siswa"):
            npm = st.text_input("Nomor Pokok Mahasiswa (NPM)")
            nama = st.text_input("Nama Lengkap Mahasiswa")
            kelas = st.text_input("Kelas", value="INF26B", disabled=True)
            
            btn_tambah = st.form_submit_button("Tambah ke Daftar")
            
            if btn_tambah:
                if npm and nama:
                    if npm in df_siswa["NPM"].astype(str).values:
                        st.error("⚠️ NPM tersebut sudah terdaftar!")
                    else:
                        df_baru = pd.DataFrame({"NPM": [npm], "Nama": [nama], "Kelas": ["INF26B"]})
                        df_siswa = pd.concat([df_siswa, df_baru], ignore_index=True)
                        df_siswa.to_csv(DATA_SISWA_FILE, index=False)
                        st.success(f"✨ Mahasiswa **{nama}** berhasil ditambahkan!")
                        st.rerun()
                else:
                    st.warning("⚠️ Semua kolom wajib diisi!")
    
    with col2:
        st.subheader("📋 Daftar Mahasiswa Aktif")
        st.dataframe(df_siswa, use_container_width=True)
        
        if not df_siswa.empty:
            st.markdown("---")
            npm_hapus = st.selectbox("Pilih NPM Mahasiswa yang Ingin Dihapus", df_siswa["NPM"].astype(str))
            if st.button("🗑️ Hapus Mahasiswa Terpilih"):
                df_siswa = df_siswa[df_siswa["NPM"].astype(str) != str(npm_hapus)]
                df_siswa.to_csv(DATA_SISWA_FILE, index=False)
                st.success("🗑️ Data mahasiswa berhasil dihapus!")
                st.rerun()

# ==================== MENU 3: REKAP & LAPORAN ====================
elif menu == "📊 Rekap & Statistik":
    st.header("📊 Rekapitulasi & Statistik Kehadiran")
    
    df_absen = pd.read_csv(DATA_ABSENSI_FILE)
    
    if df_absen.empty:
        st.info("ℹ️ Belum ada data absensi yang tercatat. Silakan lakukan pencatatan presensi terlebih dahulu.")
    else:
        semua_matkul = list(df_absen["Mata Kuliah"].unique())
        pilihan_matkul_rekap = st.selectbox("🔍 Filter Berdasarkan Mata Kuliah", ["Semua Mata Kuliah"] + semua_matkul)
        
        if pilihan_matkul_rekap != "Semua Mata Kuliah":
            df_filtered = df_absen[df_absen["Mata Kuliah"] == pilihan_matkul_rekap]
        else:
            df_filtered = df_absen
            
        st.markdown("### 📄 Tabel Riwayat Kehadiran")
        st.dataframe(df_filtered, use_container_width=True)
        
        st.markdown("### 📈 Grafik & Statistik Kehadiran")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        total_data = len(df_filtered)
        hadir_cnt = len(df_filtered[df_filtered["Status"] == "Hadir"]) if total_data > 0 else 0
        izin_cnt = len(df_filtered[df_filtered["Status"] == "Izin"]) if total_data > 0 else 0
        sakit_cnt = len(df_filtered[df_filtered["Status"] == "Sakit"]) if total_data > 0 else 0
        
        col_m1.metric("Total Presensi", total_data)
        col_m2.metric("Total Hadir", hadir_cnt)
        col_m3.metric("Total Izin", izin_cnt)
        col_m4.metric("Total Sakit", sakit_cnt)
        
        status_counts = df_filtered["Status"].value_counts()
        st.bar_chart(status_counts)
        
        st.markdown("---")
        st.subheader("📥 Unduh Laporan")
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Rekap Data (CSV)",
            data=csv_data,
            file_name=f"rekap_absensi_{pilihan_matkul_rekap.replace(' ', '_')}.csv",
            mime="text/csv",
        )