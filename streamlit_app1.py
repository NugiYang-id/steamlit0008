import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide")

# URL dari Google Apps Script
URL = "https://script.google.com/macros/s/AKfycby30tk6HJkxDQM9EYmMsmuzcvSLK4TuChyz00FLKQnxncJ8tiysKdLrSb9eisUVUVwp5g/exec"

# Fungsi untuk mengambil data dari Google Apps Script
def fetch_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Fungsi untuk menambahkan data
def add_data(name, area, line, trouble):
    response = requests.post(URL, json={"action": "add", "name": name, "area": area, "line": line, "trouble": trouble})
    return response.text  # Kembalikan respons untuk debugging

# Fungsi untuk mengupdate data
def update_data(name, area, line, trouble):
    response = requests.post(URL, json={"action": "update", "name": name, "area": area, "line": line, "trouble": trouble})
    return response.text

# Fungsi untuk menghapus data
def delete_data(name):
    response = requests.post(URL, json={"action": "delete", "name": name})
    if response.status_code == 200 and "Deleted" in response.text:
        return "Deleted"
    else:
        return response.text

# Mengambil data
data = fetch_data()

# Konversi ke DataFrame
if data:
    df = pd.DataFrame(data)
else:
    df = pd.DataFrame(columns=["name", "area", "line", "trouble"])

# Membuat Dashboard dengan Streamlit
st.title("Dashboard Data Pengguna")

# Tombol untuk refresh data
if st.button("Muat Ulang Data"):
    data = fetch_data()
    df = pd.DataFrame(data)

# Menampilkan DataFrame
st.write("### Data dari Google Sheets")
st.dataframe(df)

# Form untuk menambah data
st.write("### Tambah Data")
with st.form("add_form"):
    new_name = st.text_input("Nama")
    new_area = st.text_input("Area")
    new_line = st.text_input("Line")
    new_trouble = st.text_input("Trouble")

    submitted = st.form_submit_button("Tambah")
    if submitted:
        result = add_data(new_name, new_area, new_line, new_trouble)
        if "Success" in result:
            st.success("Data berhasil ditambahkan!")
            st.rerun()
        else:
            st.error(f"Terjadi kesalahan: {result}")

# Form untuk mengupdate data
st.write("### Update Data")
with st.form("update_form"):
    update_name = st.selectbox("Pilih Nama", df["name"].unique())
    update_area = st.text_input("Area Baru")
    update_line = st.text_input("Line Baru")
    update_trouble = st.text_input("Trouble Baru")
    update_submitted = st.form_submit_button("Update")
    if update_submitted:
        result = update_data(update_name, update_area, update_line, update_trouble)
        if "Updated" in result:
            st.success("Data berhasil diperbarui!")
            st.rerun()
        else:
            st.error(f"Terjadi kesalahan: {result}")

# Form untuk menghapus data
st.write("### Hapus Data")
with st.form("delete_form"):
    delete_name = st.selectbox("Pilih Nama untuk Dihapus", df["name"].unique())
    delete_submitted = st.form_submit_button("Hapus")
    if delete_submitted:
        result = delete_data(delete_name)
        if "Deleted" in result:
            st.success("Data berhasil dihapus!")
            st.rerun()
        else:
            st.error(f"Terjadi kesalahan: {result}")