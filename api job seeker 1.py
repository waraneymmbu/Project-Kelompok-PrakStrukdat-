import streamlit as st
import requests

st.title("💼 Job Search via Arbeitnow API")

st.write("API ini mengambil data dari Arbeitnow Job Board (Eropa).")

keyword = st.text_input("Kata kunci pekerjaan", "software engineer")
page = st.number_input("Halaman (page)", min_value=1, value=1)

if st.button("Cari Lowongan"):
    url = f"https://www.arbeitnow.com/api/job-board-api?page={page}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        jobs = data.get("data", [])
        filtered = [job for job in jobs if keyword.lower() in job["title"].lower()]
        
        if filtered:
            st.success(f"Ditemukan {len(filtered)} lowongan di halaman {page}:")
            for job in filtered:
                st.markdown(f"### [{job['title']}]({job['url']})")
                st.write(f"🏢 {job.get('company_name', 'Tidak disebutkan')}")
                st.write(f"📍 {job.get('location', 'Lokasi tidak tersedia')}")
                st.write(job.get("description", "")[:300] + "...")
                st.divider()
        else:
            st.warning("Tidak ada hasil cocok dengan kata kunci.")
    else:
        st.error(f"Gagal mengambil data. Status: {response.status_code}")
