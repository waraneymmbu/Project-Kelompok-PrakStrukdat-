import streamlit as st
import requests
import math
import random

COLUMNS_PER_ROW = 3 
ITEMS_PER_PAGE = 9 

@st.cache_data
def fetch_api_jobs(keyword=""):
    url = "https://www.arbeitnow.com/api/job-board-api"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        jobs_raw = data.get("data", [])

        jobs_list = []
        for i, job in enumerate(jobs_raw):

            if keyword.lower() not in job["title"].lower():
                continue

            jobs_list.append({
                "ID": i + 1,
                "Posisi": job.get("title", "-"),
                "Perusahaan": job.get("company_name", "-"),
                "Lokasi": job.get("location", "-"),
                "Tanggal Posting": job.get("created_at", "-"),
                "URL": job.get("url", "-"),

                "Gaji_Num": random.randint(6, 35),
            })

        return jobs_list

    except Exception as e:
        st.error(f"Gagal mengakses API: {e}")
        return []

def search_jobs_page(get_jobs, current_page_num):

    st.title("Cari Lowongan Kerja")
    st.write("Temukan pekerjaan berdasarkan kata kunci.")

    search_term = st.text_input("Masukkan kata kunci pekerjaan...", st.session_state.get("search_term", ""))

    if st.button("Cari", use_container_width=True):
        st.session_state["search_term"] = search_term
        st.session_state["search_page"] = 1
        st.rerun()

    keyword = st.session_state.get("search_term", "")
    jobs_list = fetch_api_jobs(keyword)

    st.write(f"Menampilkan **{len(jobs_list)} hasil** untuk kata kunci: `{keyword}`")

    total_items = len(jobs_list)
    total_pages = max(1, math.ceil(total_items / ITEMS_PER_PAGE))

    st.session_state["search_page"] = max(1, min(st.session_state["search_page"], total_pages))
    page = st.session_state["search_page"]

    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    jobs_to_display = jobs_list[start_idx:end_idx]

    num_rows_current_page = math.ceil(len(jobs_list) / COLUMNS_PER_ROW)

    for row in range(num_rows_current_page):
        cols = st.columns(COLUMNS_PER_ROW)

        for col_index in range(COLUMNS_PER_ROW):
            job_index = (row * COLUMNS_PER_ROW) + col_index

            if job_index < len(jobs_list):
                job = jobs_list[job_index]

                with cols[col_index], st.container(border=True):

                    st.markdown(
                        f"<span style='color:#00B14F; font-weight:700; font-size:16px;'>{job['Perusahaan']}</span><hr>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<div style='font-size:15px; font-weight:600;'>{job['Posisi']}</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"<p style='font-size: small; color: gray;'>"
                        f"Lokasi: {job['Lokasi']} | {job['Tanggal Posting']}"
                        f"</p>",
                        unsafe_allow_html=True
                    )

                    if 'Tags' in job:
                        st.markdown(
                            f"<b>Tags:</b> {job['Tags']}",
                            unsafe_allow_html=True
                        )
                    st.button(
                        "Lihat Detail",
                        key=f"detail_{job['ID']}_{current_page_num}_{job_index}",
                        use_container_width=True
                    )
