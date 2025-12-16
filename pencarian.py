import streamlit as st
import requests
import math
import random

COLUMNS_PER_ROW = 3
ITEMS_PER_PAGE = 9

API_KEY = "9fa2489c-9d2f-4c58-9cb7-693afc2aab36"
API_URL = f"https://jooble.org/api/{API_KEY}"

@st.cache_data
def fetch_api_jobs(keyword="", location_filter=""):
    try:
        payload = {
            "keywords": keyword,
            "page": 1,
            "size": 50
        }

        if location_filter.strip() != "":
            payload["location"] = location_filter.strip()

        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()

        data = response.json()
        jobs_raw = data.get("jobs", [])

        jobs_list = []
        for i, job in enumerate(jobs_raw):
            jobs_list.append({
                "ID": i + 1,
                "Posisi": job.get("title", "-"),
                "Perusahaan": job.get("company", "-"),
                "Lokasi": job.get("location", "-"),
                "Tanggal_Update": job.get("updated", "-"),
                "URL": job.get("link", "-"),
                "Gaji_Num": random.randint(6, 35),
            })

        return jobs_list

    except Exception as e:
        st.error(f"Gagal mengakses API Jooble: {e}")
        return []


def search_jobs_page(get_jobs, current_page_num):

    st.title("Cari Lowongan Kerja")

    search_term = st.text_input(
        "Masukkan kata kunci pekerjaan",
        st.session_state.get("search_term", "")
    )

    location_term = st.text_input(
        "Filter lokasi (opsional)",
        st.session_state.get("location_term", "")
    )

    if st.button("Cari", use_container_width=True):
        st.session_state["search_term"] = search_term
        st.session_state["location_term"] = location_term
        st.session_state["search_page"] = 1
        st.session_state["selected_job"] = None
        st.session_state["has_searched"] = True  # Flag untuk menandai sudah search
        st.rerun()

    # Cek apakah user sudah pernah klik tombol "Cari"
    if not st.session_state.get("has_searched", False):
        st.info("Masukkan kata kunci untuk melihat lowongan kerja.")
        return  # Stop eksekusi, tidak fetch API

    keyword = st.session_state.get("search_term", "")
    location_filter = st.session_state.get("location_term", "")
    
    # API hanya dipanggil jika has_searched = True
    jobs_list = fetch_api_jobs(keyword, location_filter)

    st.write(f"Menampilkan **{len(jobs_list)} hasil** | Kata kunci: `{keyword}` | Lokasi: `{location_filter}`")

    if len(jobs_list) == 0:
        st.warning("Tidak ada hasil yang ditemukan. Coba kata kunci lain.")
        return

    total_items = len(jobs_list)
    total_pages = max(1, math.ceil(total_items / ITEMS_PER_PAGE))

    st.session_state["search_page"] = max(1, min(st.session_state["search_page"], total_pages))
    page = st.session_state["search_page"]

    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    jobs_to_display = jobs_list[start_idx:end_idx]

    num_rows_current_page = math.ceil(len(jobs_to_display) / COLUMNS_PER_ROW)

    for row in range(num_rows_current_page):
        cols = st.columns(COLUMNS_PER_ROW)

        for col_index in range(COLUMNS_PER_ROW):
            job_index = (row * COLUMNS_PER_ROW) + col_index

            if job_index < len(jobs_to_display):
                job = jobs_to_display[job_index]

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
                        f"Lokasi: {job['Lokasi']}<br>"
                        f"Tanggal update: {job['Tanggal_Update']}"
                        f"</p>",
                        unsafe_allow_html=True
                    )

                    st.link_button(
                        "Lihat Detail",
                        url=job["URL"],
                        use_container_width=True
                    )

    st.write("")

    col_prev, col_page, col_next = st.columns([1, 2, 1])

    with col_prev:
        if st.button("◀ Sebelumnya", disabled=(page <= 1)):
            st.session_state["search_page"] -= 1
            st.rerun()

    with col_page:
        st.markdown(f"<center>Halaman {page} / {total_pages}</center>", unsafe_allow_html=True)

    with col_next:
        if st.button("Selanjutnya ▶", disabled=(page >= total_pages)):
            st.session_state["search_page"] += 1
            st.rerun()
