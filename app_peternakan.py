import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, date
import json
import os
import uuid

DATA_FILE = "keuangan_peternakan_streamlit.json"
LOGO_PATH = "Sapi.png" 

def set_css_style():
    st.markdown(
        f"""
        <style>
            /* Sidebar logo container */
            .sidebar-logo-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px 0 10px 0;
                border-bottom: 2px solid #FF7F50;
                margin-bottom: 20px;
            }}
            .sidebar-logo-caption {{
                font-weight: 700;
                color: #FF7F50;
                margin-top: 8px;
                font-size: 18px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
            }}

            /* Sidebar base */
            [data-testid="stSidebar"] > div:first-child {{
                padding-top: 0.5rem;
            }}
            .css-1d391kg {{
                background-color: #1E90FF;
                color: white;
            }}
            .css-1d391kg h2, .css-1d391kg label {{
                color: white;
            }}
            .css-1d391kg .st-bx {{
                color: white;
            }}

            /* Sidebar menu item hover */
            [data-testid="stSidebarNav"] div[role="listitem"]:hover {{
                background-color: #FF7F50 !important;
                color: white !important;
                cursor: pointer;
                border-radius: 8px;
            }}

            /* Buttons */
            div.stButton > button {{
                background-color: #1E90FF;
                color: white;
                border-radius: 10px;
                height: 3em;
                font-weight: bold;
                border: none;
                box-shadow: 2px 4px 8px rgb(255 127 80 / 0.4);
                transition: background-color 0.3s ease;
                width: 100%;
            }}
            div.stButton > button:hover {{
                background-color: #FF7F50;
            }}

            /* Section headers */
            .section-header {{
                background-color: #1E90FF;
                color: white;
                padding: 12px 16px;
                border-radius: 10px;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 12px;
            }}

            /* Tables */
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th {{
                background-color: #1E90FF !important;
                color: white !important;
                padding: 8px !important;
            }}
            td {{
                border-bottom: 1px solid #ddd !important;
                padding: 8px !important;
                color: #0B3D91 !important;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9 !important;
            }}
            tr:hover {{
                background-color: #FF7F50 !important;
                color: white !important;
            }}

            /* Highlights */
            .orange-text {{
                color: #FF7F50;
                font-weight: 600;
            }}

            /* Alert messages */
            div.stAlert > div[data-testid="stMarkdownContainer"] p {{
                font-weight: 600;
            }}

            /* Body background */
            .main .block-container {{
                background-color: #F0F8FF;
                color: #0B3D91;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
        </style>
        """, unsafe_allow_html=True
    )

def sidebar_centered_logo():
    if os.path.exists(LOGO_PATH):
        img_bytes = open(LOGO_PATH, "rb").read()
        st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
        st.image(img_bytes, width=140)
        st.markdown('<div class="sidebar-logo-caption">Sistem Akuntansi Peternakan<br><small>Sapi Perah Ungaran</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #FF7F50; font-weight:600; text-align:center'>Logo tidak ditemukan di path.</p>", unsafe_allow_html=True)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"jurnal_umum": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def tambah_jurnal_umum(data):
    st.markdown('<div class="section-header">Tambah Jurnal Umum</div>', unsafe_allow_html=True)

    daftar_akun = [
        "Kas", "Bank", "Piutang", "Hutang",
        "Hutang Karyawan", "Hutang Pajak",
        "Penjualan Susu",  
        "Pendapatan dari Penjualan Perlengkapan",
        "Pendapatan dari Penjualan Tanah",
        "Pendapatan Saham",
        "Biaya Pakan", "Biaya Obat", "Biaya Listrik",
        "Biaya Air",
        "Beban Pokok Pendapatan", "Biaya Operasional",
        "Biaya Amortisasi Pajak", "Biaya Depresiasi Kendaraan", "Biaya Depresiasi Bangunan",
        "Biaya Pembelian Perlengkapan", "Biaya Pembelian Tanah",
        "Biaya Pembelian Kendaraan", "Biaya Pembelian Bangunan",
        "Biaya Dividen",
        "Persediaan"
    ]

    #=== FORM TANPA SUBMIT BUTTON ===#
    with st.form("form_jurnal"):
        tanggal = st.date_input("Tanggal", value=date.today())
        deskripsi = st.text_input("Deskripsi Transaksi")

        baris_entri = st.number_input("Jumlah Entri Akun", min_value=2, max_value=20, value=2, step=1)

        # input disimpan dulu terpisah
        input_akun = []
        input_debit = []
        input_kredit = []

        for i in range(baris_entri):
            st.markdown(f"*Entri {i+1}*")

            input_akun.append(
                st.selectbox(
                    f"akun{i+1}",
                    daftar_akun,
                    key=f"akun_input_{i}"
                )
            )
            input_debit.append(
                st.number_input(
                    f"debit{i+1} (Rp)",
                    min_value=0.0,
                    format="%.2f",
                    key=f"debit_input_{i}"
                )
            )
            input_kredit.append(
                st.number_input(
                    f"kredit{i+1} (Rp)",
                    min_value=0.0,
                    format="%.2f",
                    key=f"kredit_input_{i}"
                )
            )

        # Tidak ada tombol submit dalam form

        #=== SUBMIT DIBUAT DI LUAR FORM ===#
        submit = st.form_submit_button("Simpan Jurnal")
        

    if submit:
        # validasi dan simpan jurnal
        if not deskripsi.strip():
            st.warning("Deskripsi transaksi tidak boleh kosong.")
            return
            
        entri = []
        for idx in range(baris_entri):
            akun = input_akun[idx]
            debit = input_debit[idx]
            kredit = input_kredit[idx]

            if debit > 0 and kredit > 0:
                st.warning(f"Pada entri {idx+1}, kolom Debit dan Kredit tidak boleh diisi bersamaan.")
                return
                
            if debit > 0 or kredit > 0:
                entri.append({"akun": akun, "debit": debit, "kredit": kredit})

        total_debit = sum(e["debit"] for e in entri)
        total_kredit = sum(e["kredit"] for e in entri)

        if total_debit == 0 and total_kredit == 0:
            st.warning("Masukkan minimal satu nominal debit atau kredit.")
        elif abs(total_debit - total_kredit) > 0.01:
            st.warning(f"Total Debit (Rp {total_debit:,.2f}) tidak sama dengan Total Kredit (Rp {total_kredit:,.2f}).")
            return
            
        jurnal_baru = {
            "id": str(uuid.uuid4()),
            "tanggal": tanggal.strftime("%Y-%m-%d"),
            "deskripsi": deskripsi.strip(),
            "entri": [e for e in entri if e["debit"] > 0 or e["kredit"] > 0]
        }
        data["jurnal_umum"].append(jurnal_baru)
        save_data(data)
        st.success("Jurnal berhasil disimpan.")


def edit_jurnal_form(data, jurnal_id):
    jurnal = next((j for j in data["jurnal_umum"] if j["id"] == jurnal_id), None)
    if not jurnal:
        st.error("Jurnal tidak ditemukan.")
        return

    st.markdown('<div class="section-header">Edit Jurnal Umum</div>', unsafe_allow_html=True)

    with st.form(f"form_edit_{jurnal_id}"):
        tanggal = st.date_input("Tanggal", datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date())
        deskripsi = st.text_input("Deskripsi Transaksi", value=jurnal["deskripsi"])

        daftar_akun = [
            "Kas", "Bank", "Piutang", "Hutang",
            "Hutang Karyawan", "Hutang Pajak",
            "Penjualan Susu",  
            "Pendapatan dari Penjualan Perlengkapan",
            "Pendapatan dari Penjualan Tanah",
            "Pendapatan Saham",
            "Biaya Pakan", "Biaya Obat", "Biaya Listrik",
            "Biaya Air",
            "Beban Pokok Pendapatan", "Biaya Operasional",
            "Biaya Amortisasi Pajak", "Biaya Depresiasi Kendaraan", "Biaya Depresiasi Bangunan",
            "Biaya Pembelian Perlengkapan", "Biaya Pembelian Tanah",
            "Biaya Pembelian Kendaraan", "Biaya Pembelian Bangunan",
            "Biaya Dividen",
            "Persediaan"
        ]

        baris_entri = len(jurnal["entri"])
        baris_entri = st.number_input("Jumlah Entri Akun", min_value=2, max_value=20, value=baris_entri, step=1)

        entri_baru = []
        for i in range(baris_entri):
            st.markdown(f"*Entri {i+1}*")
            akun_default = jurnal["entri"][i]["akun"] if i < len(jurnal["entri"]) else daftar_akun[0]
            debit_default = jurnal["entri"][i]["debit"] if i < len(jurnal["entri"]) else 0.0
            kredit_default = jurnal["entri"][i]["kredit"] if i < len(jurnal["entri"]) else 0.0

            akun = st.selectbox(f"Akun {i+1}", daftar_akun, index=daftar_akun.index(akun_default), key=f"edit_akun_{jurnal_id}_{i}")
            debit = st.number_input(f"Debit {i+1} (Rp)", min_value=0.0, format="%.2f", value=debit_default, key=f"edit_debit_{jurnal_id}_{i}")
            kredit = st.number_input(f"Kredit {i+1} (Rp)", min_value=0.0, format="%.2f", value=kredit_default, key=f"edit_kredit_{jurnal_id}_{i}")
            entri_baru.append({"akun": akun, "debit": debit, "kredit": kredit})

        submit = st.form_submit_button("Update Jurnal")

        if submit:
            if not deskripsi.strip():
                st.warning("Deskripsi transaksi tidak boleh kosong.")
                return

            for idx, e in enumerate(entri_baru):
                if e["debit"] > 0 and e["kredit"] > 0:
                    st.warning(f"Pada entri {idx+1}, kolom Debit dan Kredit tidak boleh diisi bersamaan.")
                    return

            total_debit = sum(e["debit"] for e in entri_baru)
            total_kredit = sum(e["kredit"] for e in entri_baru)
            if total_debit == 0 and total_kredit == 0:
                st.warning("Masukkan minimal satu nominal debit atau kredit.")
            elif abs(total_debit - total_kredit) > 0.01:
                st.warning(f"Total debit (Rp {total_debit:,.2f}) dan kredit (Rp {total_kredit:,.2f}) harus sama.")
            else:
                jurnal["tanggal"] = tanggal.strftime("%Y-%m-%d")
                jurnal["deskripsi"] = deskripsi.strip()
                jurnal["entri"] = [e for e in entri_baru if e["debit"] > 0 or e["kredit"] > 0]
                save_data(data)
                st.session_state.pop("edit_jurnal_id", None)
                st.success("Jurnal berhasil diperbarui.")
                st.rerun()


def lihat_jurnal_umum(data):
    st.markdown('<div class="section-header">Daftar Jurnal Umum</div>', unsafe_allow_html=True)

    if "edit_jurnal_id" in st.session_state:
        edit_jurnal_form(data, st.session_state["edit_jurnal_id"])
        st.write("---")

    if not data["jurnal_umum"]:
        st.info("Belum ada jurnal umum.")
        return

    jurnal_urut = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"], reverse=True)

    for jurnal in jurnal_urut:
        st.markdown(f"*Tanggal:* <span class='orange-text'>{jurnal['tanggal']}</span>  |  *Deskripsi:* {jurnal['deskripsi']}", unsafe_allow_html=True)

        cols = st.columns([6, 1, 1])

        with cols[0]:
            table_md = """
| Akun | Debit (Rp) | Kredit (Rp) |
|-------|------------|-------------|
"""
            for e in jurnal["entri"]:
                debit_str = f"{e['debit']:,.2f}" if e["debit"] else ""
                kredit_str = f"{e['kredit']:,.2f}" if e["kredit"] else ""
                table_md += f"| {e['akun']} | {debit_str} | {kredit_str} |\n"
            st.markdown(table_md)

        with cols[1]:
            if st.button("Edit", key=f"edit_{jurnal['id']}"):
                st.session_state["edit_jurnal_id"] = jurnal["id"]
                st.rerun()

        # tombol hapus pertama
        with cols[2]:
            if st.button("Hapus", key=f"hapus_{jurnal['id']}"):
                st.session_state[f"konfirmasi_{jurnal['id']}"] = True
                st.rerun()

        # jika user menekan hapus → tampilkan konfirmasi
        if st.session_state.get(f"konfirmasi_{jurnal['id']}", False):
            
            st.warning(f"Yakin ingin menghapus jurnal tanggal {jurnal['tanggal']} ?")

            col_konfirmasi = st.columns(2)

            # Tombol YA
            if col_konfirmasi[0].button("Ya, hapus", key=f"ya_hapus_{jurnal['id']}"):
                data["jurnal_umum"] = [
                    j for j in data["jurnal_umum"] if j["id"] != jurnal["id"]
                ]
                save_data(data)
                st.success("Jurnal berhasil dihapus.")
                st.session_state[f"konfirmasi_{jurnal['id']}"] = False
                st.rerun()

            # Tombol BATAL
            if col_konfirmasi[1].button("Batal", key=f"batal_hapus_{jurnal['id']}"):
                st.session_state[f"konfirmasi_{jurnal['id']}"] = False
                st.rerun()


def buku_besar(data):
    st.markdown('<div class="section-header">Buku Besar</div>', unsafe_allow_html=True)

    if not data["jurnal_umum"]:
        st.info("Belum ada data jurnal umum.")
        return

    akun_set = set()
    for jurnal in data["jurnal_umum"]:
        for e in jurnal["entri"]:
            akun_set.add(e["akun"])
    daftar_akun = sorted(list(akun_set))

    akun_terpilih = st.selectbox("Pilih Akun", daftar_akun)

    jurnal_sorted = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"])
    tgl_awal_default = datetime.strptime(jurnal_sorted[0]["tanggal"], "%Y-%m-%d").date() if jurnal_sorted else date.today()
    col1, col2 = st.columns(2)
    with col1:
        tgl_mulai = st.date_input("Dari Tanggal", value=tgl_awal_default)
    with col2:
        tgl_akhir = st.date_input("Sampai Tanggal", value=date.today())

    if tgl_akhir < tgl_mulai:
        st.warning("Tanggal akhir harus sama atau setelah tanggal mulai.")
        return

    entri_akun = []
    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        if not (tgl_mulai <= tgl <= tgl_akhir):
            continue
        for e in jurnal["entri"]:
            if e["akun"] == akun_terpilih:
                entri_akun.append({
                    "tanggal": jurnal["tanggal"],
                    "deskripsi": jurnal["deskripsi"],
                    "debit": e["debit"],
                    "kredit": e["kredit"]
                })

    if not entri_akun:
        st.warning(f"Tidak ada mutasi pada akun '{akun_terpilih}' untuk periode ini.")
        return

    saldo = 0.0
    rows = []
    for e in sorted(entri_akun, key=lambda x: x["tanggal"]):
        saldo += e["debit"] - e["kredit"]
        rows.append({
            "Tanggal": e["tanggal"],
            "Deskripsi": e["deskripsi"],
            "Debit": f"Rp {e['debit']:,.2f}" if e["debit"] else "",
            "Kredit": f"Rp {e['kredit']:,.2f}" if e["kredit"] else "",
            "Saldo": f"Rp {saldo:,.2f}"
        })

    st.markdown(f"### Mutasi Akun: <span class='orange-text'>{akun_terpilih}</span>", unsafe_allow_html=True)
    df = pd.DataFrame(rows)
    st.table(df)


def neraca_saldo(data):
    st.markdown('<div class="section-header">Neraca Saldo</div>', unsafe_allow_html=True)

    if not data["jurnal_umum"]:
        st.info("Belum ada data jurnal umum.")
        return

    jurnal_sorted = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"])
    tgl_awal_default = datetime.strptime(jurnal_sorted[0]["tanggal"], "%Y-%m-%d").date() if jurnal_sorted else date.today()
    col1, col2 = st.columns(2)
    with col1:
        tgl_mulai = st.date_input("Dari Tanggal", value=tgl_awal_default)
    with col2:
        tgl_akhir = st.date_input("Sampai Tanggal", value=date.today())

    if tgl_akhir < tgl_mulai:
        st.warning("Tanggal akhir harus sama atau setelah tanggal mulai.")
        return

    akun_set = set()
    for jurnal in data["jurnal_umum"]:
        for e in jurnal["entri"]:
            akun_set.add(e["akun"])

    saldo_per_akun = {}
    for akun in akun_set:
        saldo_per_akun[akun] = {"debit": 0.0, "kredit": 0.0}

    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        if not (tgl_mulai <= tgl <= tgl_akhir):
            continue
        for e in jurnal["entri"]:
            saldo_per_akun[e["akun"]]["debit"] += e["debit"]
            saldo_per_akun[e["akun"]]["kredit"] += e["kredit"]

    rows = []
    total_debit = 0.0
    total_kredit = 0.0

    for akun in sorted(saldo_per_akun.keys()):
        debit = saldo_per_akun[akun]["debit"]
        kredit = saldo_per_akun[akun]["kredit"]
        saldo = debit - kredit

        saldo_debit = saldo if saldo > 0 else 0
        saldo_kredit = -saldo if saldo < 0 else 0

        total_debit += saldo_debit
        total_kredit += saldo_kredit

        rows.append({
            "Akun": akun,
            "Saldo Debit (Rp)": f"Rp {saldo_debit:,.2f}" if saldo_debit else "",
            "Saldo Kredit (Rp)": f"Rp {saldo_kredit:,.2f}" if saldo_kredit else ""
        })

    df = pd.DataFrame(rows)
    st.table(df)

    st.markdown("---")
    st.markdown(f"<p class='orange-text'><b>Total Saldo Debit:</b> Rp {total_debit:,.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='orange-text'><b>Total Saldo Kredit:</b> Rp {total_kredit:,.2f}</p>", unsafe_allow_html=True)

    if abs(total_debit - total_kredit) > 0.01:
        st.error("⚠ Neraca Saldo tidak seimbang! Total Debit tidak sama dengan Total Kredit.")
    else:
        st.success("Neraca Saldo seimbang (Total Debit = Total Kredit).")


def laporan_laba_rugi(data):
    st.markdown('<div class="section-header">Proyeksi Laporan Laba Rugi</div>', unsafe_allow_html=True)
    st.markdown("Untuk Periode yang berakhir")

    jurnal_sorted = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"])
    if not jurnal_sorted:
        st.info("Belum ada data jurnal umum.")
        return

    tgl_awal_default = datetime.strptime(jurnal_sorted[0]["tanggal"], "%Y-%m-%d").date()
    col1, col2 = st.columns(2)
    with col1:
        tgl_mulai = st.date_input("Dari Tanggal", value=tgl_awal_default)
    with col2:
        tgl_akhir = st.date_input("Sampai Tanggal", value=date.today())

    if tgl_akhir < tgl_mulai:
        st.warning("Tanggal akhir harus sama atau setelah tanggal mulai.")
        return

    akun_pendapatan = {
        "Penjualan Susu",
        "Pendapatan dari Penjualan Perlengkapan",
        "Pendapatan dari Penjualan Tanah",
        "Pendapatan Saham"
    }

    akun_harga_pokok_penjualan = {
        "Beban Pokok Pendapatan",
    }
    akun_beban = {
        "Biaya Pakan",
        "Biaya Obat",
        "Biaya Listrik",
        "Biaya Air",
        "Biaya Operasional",
        "Biaya Amortisasi Pajak",
        "Biaya Depresiasi Kendaraan",
        "Biaya Depresiasi Bangunan"
    }

    total_pendapatan = 0.0
    total_persediaan_awal = 0.0
    total_persediaan_akhir = 0.0
    total_harga_pokok_penjualan = 0.0
    total_beban = 0.0

    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        for e in jurnal["entri"]:
            akun = e["akun"]
            debit = e["debit"]
            kredit = e["kredit"]

            if akun == "Persediaan":
                if tgl < tgl_mulai:
                    total_persediaan_awal += debit - kredit
                elif tgl <= tgl_akhir:
                    total_persediaan_akhir += debit - kredit

    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        if not (tgl_mulai <= tgl <= tgl_akhir):
            continue
        for e in jurnal["entri"]:
            akun = e["akun"]
            debit = e["debit"]
            kredit = e["kredit"]

            if akun in akun_pendapatan:
                total_pendapatan += kredit - debit
            elif akun in akun_harga_pokok_penjualan:
                total_harga_pokok_penjualan += debit - kredit
            elif akun in akun_beban:
                total_beban += debit - kredit

    hpp = total_harga_pokok_penjualan + total_persediaan_awal - total_persediaan_akhir
    laba_kotor = total_pendapatan - hpp
    laba_rugi_bersih = laba_kotor - total_beban

    laba_str = f"Rp {abs(laba_rugi_bersih):,.2f}"
    if laba_rugi_bersih >= 0:
        warna = "#1E90FF"
        status = "Laba Bersih"
    else:
        warna = "#FF7F50"
        status = "Rugi Bersih"

    laporan_md = f"""
| Keterangan                                         | Nilai (Rp)           |
|---------------------------------------------------|----------------------|
| *Pendapatan*                                     |                      |
| {'<br>'.join(akun_pendapatan)}                    |                      |
| Total Pendapatan                                   | Rp {total_pendapatan:,.2f}   |
|                                                   |                      |
| *Persediaan Awal*                                | Rp {total_persediaan_awal:,.2f}   |
| *Pembelian (Beban Pokok Pendapatan)*            | Rp {total_harga_pokok_penjualan:,.2f}   |
| *Persediaan Akhir*                               | Rp {total_persediaan_akhir:,.2f}   |
| *Harga Pokok Penjualan (HPP)*                    | *Rp {hpp:,.2f}*   |
| *Laba Kotor*                                     | *Rp {laba_kotor:,.2f}* |
|                                                   |                      |
| *Beban*                                          |                      |
| Total Beban                                        | Rp {total_beban:,.2f}   |
|                                                   |                      |
| <span style="color:{warna};"><b>Proyeksi {status}</b></span> | <span style="color:{warna};"><b>{laba_str}</b></span>   |
"""
    st.markdown(laporan_md, unsafe_allow_html=True)


def laporan_arus_kas_terperinci(data):
    st.markdown('<div class="section-header">Laporan Arus Kas Terperinci</div>', unsafe_allow_html=True)
    st.markdown("Laporan arus kas berdasarkan aktivitas operasi, investasi, dan pendanaan")

    if not data["jurnal_umum"]:
        st.info("Belum ada data jurnal umum.")
        return

    jurnal_sorted = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"])
    tgl_awal_default = datetime.strptime(jurnal_sorted[0]["tanggal"], "%Y-%m-%d").date()
    col1, col2 = st.columns(2)
    with col1:
        tgl_mulai = st.date_input("Dari Tanggal", value=tgl_awal_default)
    with col2:
        tgl_akhir = st.date_input("Sampai Tanggal", value=date.today())

    if tgl_akhir < tgl_mulai:
        st.warning("Tanggal akhir harus sama atau setelah tanggal mulai.")
        return

    aktivitas_operasi = {
        "Pendapatan Bersih": ["Penjualan Susu", "Pendapatan dari Penjualan Perlengkapan", "Pendapatan dari Penjualan Tanah"],
        "Kenaikan Piutang": ["Piutang"],
        "Kenaikan Utang Usaha": ["Hutang"],
        "Kenaikan Utang Karyawan": ["Hutang Karyawan"],
        "Kenaikan Utang Pajak": ["Hutang Pajak"],
        "Keuntungan Dari Penjualan Perlengkapan": ["Pendapatan dari Penjualan Perlengkapan"],
        "Keuntungan Dari Penjualan Tanah": ["Pendapatan dari Penjualan Tanah"],
        "Beban Amortisasi Pajak": ["Biaya Amortisasi Pajak"],
        "Beban Depresiasi Kendaraan": ["Biaya Depresiasi Kendaraan"],
        "Beban Depresiasi Bangunan": ["Biaya Depresiasi Bangunan"],
        "Biaya Pakan": ["Biaya Pakan"],
        "Biaya Obat": ["Biaya Obat"],
        "Biaya Listrik": ["Biaya Listrik"],
        "Biaya Air": ["Biaya Air"],
        "Biaya Operasional": ["Biaya Operasional"]
    }

    aktivitas_investasi = {
        "Penjualan Perlengkapan": ["Pendapatan dari Penjualan Perlengkapan"],
        "Pembelian Perlengkapan": ["Biaya Pembelian Perlengkapan"],
        "Penjualan Tanah": ["Pendapatan dari Penjualan Tanah"],
        "Pembelian Tanah": ["Biaya Pembelian Tanah"],
        "Pembelian Kendaraan": ["Biaya Pembelian Kendaraan"],
        "Pembelian Bangunan": ["Biaya Pembelian Bangunan"]
    }

    aktivitas_pendanaan = {
        "Pembayaran Dividen": ["Biaya Dividen"],
        "Penerbitan Saham Biasa": ["Pendapatan Saham"]
    }

    def hitung_saldo(grup_akun):
        saldo_total = 0.0
        perinci = {k: 0.0 for k in grup_akun.keys()}

        for jurnal in data["jurnal_umum"]:
            tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
            if not (tgl_mulai <= tgl <= tgl_akhir):
                continue
            for e in jurnal["entri"]:
                for nama_aktivitas, akun_list in grup_akun.items():
                    if e["akun"] in akun_list:
                        arus = e["kredit"] - e["debit"]
                        perinci[nama_aktivitas] += arus
                        saldo_total += arus
        return saldo_total, perinci

    def tampilkan_tabel(judul, detail, total):
        st.markdown(f"### Aktivitas {judul}")
        if not any(nilai != 0 for nilai in detail.values()):
            st.info(f"Tidak ada transaksi pada aktivitas {judul}.")
            return

        df = pd.DataFrame({
            "Kategori": list(detail.keys()),
            "Jumlah (Rp)": [f"{v:,.2f}" for v in detail.values()]
        })
        st.table(df)

        label = "Kas Diterima" if total >= 0 else "Kas Digunakan"
        st.markdown(f"{label} dari Aktivitas {judul}:** Rp {total:,.2f}")

    saldo_op, detail_op = hitung_saldo(aktivitas_operasi)
    saldo_inv, detail_inv = hitung_saldo(aktivitas_investasi)
    saldo_pen, detail_pen = hitung_saldo(aktivitas_pendanaan)

    tampilkan_tabel("Operasi", detail_op, saldo_op)
    tampilkan_tabel("Investasi", detail_inv, saldo_inv)
    tampilkan_tabel("Pendanaan", detail_pen, saldo_pen)

    akun_kas = {"Kas", "Bank"}
    kas_awal = 0.0
    kas_akhir = 0.0
    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        for e in jurnal["entri"]:
            if e["akun"] in akun_kas:
                if tgl < tgl_mulai:
                    kas_awal += e["debit"] - e["kredit"]
                if tgl <= tgl_akhir:
                    kas_akhir += e["debit"] - e["kredit"]

    kas_bersih = saldo_op + saldo_inv + saldo_pen

    st.markdown("---")
    st.markdown(f"<p class='orange-text'><b>Kas Awal Periode ({tgl_mulai}):</b> Rp {kas_awal:,.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='orange-text'><b>Kas Bersih dari Semua Aktivitas:</b> Rp {kas_bersih:,.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='orange-text'><b>Kas Akhir Periode ({tgl_akhir}):</b> Rp {kas_akhir:,.2f}</p>", unsafe_allow_html=True)


def logout():
    st.session_state['login_status'] = False
    st.rerun()

def main():
    st.set_page_config(page_title="Sistem Akuntansi Peternakan", layout="wide")
    set_css_style()

    with st.sidebar:
        sidebar_centered_logo()

        st.title("Menu")
        menu = st.selectbox("", [
            "Tambah Jurnal Umum",
            "Lihat Jurnal Umum",
            "Buku Besar",
            "Neraca Saldo",
            "Laporan Laba Rugi",
            "Laporan Arus Kas",
            "Logout"
        ])


    import json
    import os

    USER_FILE = "users.json"

    # --- load user dari file ---
    def load_users():
        if os.path.exists(USER_FILE):
            with open("users.json", "r") as f:
                return json.load(f)
        return {}

    # --- simpan user ke file ---
    def save_users(users):
        with open("users.json", "w") as f:
            json.dump(users, f)

    if "login_status" not in st.session_state:
        st.session_state["login_status"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "login"


    users = load_users()


    # ----- REGISTER PAGE -----
    if st.session_state["page"] == "register":
        st.markdown("### Daftar Akun Baru")

        new_user = st.text_input("Buat Username")
        new_pass = st.text_input("Buat Password", type="password")

        if st.button("Daftar"):
            if not new_user:
                st.error("Username tidak boleh kosong.")
            elif new_user in users:
                st.error("Username sudah digunakan!")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("Akun berhasil dibuat! Silakan login.")
                st.session_state["page"] = "login"
                st.rerun()

        if st.button("Kembali ke Login"):
            st.session_state["page"] = "login"
            st.rerun()
        st.stop()

    # ----- LOGIN PAGE -----
    if not st.session_state["login_status"]:
        st.markdown("### Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["login_status"] = True
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Username atau password salah!")

        if st.button("Buat Akun Baru"):
            st.session_state["page"] = "register"
            st.rerun()

        st.stop()
    
    
    data = load_data()

    st.markdown(f'<div class="section-header">{menu}</div>', unsafe_allow_html=True)

    if menu == "Tambah Jurnal Umum":
        tambah_jurnal_umum(data)
    elif menu == "Lihat Jurnal Umum":
        if "edit_jurnal_id" in st.session_state:
            edit_jurnal_form(data, st.session_state["edit_jurnal_id"])
            st.write("---")
        else:
            lihat_jurnal_umum(data)
    elif menu == "Buku Besar":
        buku_besar(data)
    elif menu == "Neraca Saldo":
        neraca_saldo(data)
    elif menu == "Laporan Laba Rugi":
        laporan_laba_rugi(data)
    elif menu == "Laporan Arus Kas":
        laporan_arus_kas_terperinci(data)
    elif menu == "Logout":
        logout()

if __name__ == "__main__":
    main()