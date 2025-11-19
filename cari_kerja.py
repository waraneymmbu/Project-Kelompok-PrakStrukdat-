import streamlit as st
import pandas as pd
import math
import random # Diperlukan untuk simulasi data jika get_jobs tidak diimpor

# Konstanta untuk Pagination dan Layout
JOBS_PER_PAGE = 16 # Maksimal 16 kolom/kartu per halaman
COLUMNS_PER_ROW = 3  # Maksimal 3 kolom per baris

def search_jobs_page(get_jobs_func, current_page_num):
    """
    Halaman pencarian dan tampilan lowongan kerja dalam format kartu (card)
    dengan pembatasan 16 kartu per halaman (Pagination).
    """
    st.title("🔍 Cari Lowongan Kerja")
    
    df = get_jobs_func()
    
    # ==========================
    # 1. FILTERING
    # ==========================
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        # Gunakan session state untuk menyimpan filter agar tidak hilang saat navigasi page
        if 'search_term' not in st.session_state: st.session_state['search_term'] = ""
        if 'location_filter' not in st.session_state: st.session_state['location_filter'] = "Semua"
        
        search_txt = c1.text_input("Kata Kunci", 
                                   placeholder="Posisi atau Perusahaan", 
                                   value=st.session_state['search_term'])
        
        loc_filter = c2.selectbox("Lokasi", 
                                  ["Semua"] + list(df['Lokasi'].unique()),
                                  index=(["Semua"] + list(df['Lokasi'].unique())).index(st.session_state['location_filter']))

    # Deteksi perubahan pada filter
    if search_txt != st.session_state['search_term'] or loc_filter != st.session_state['location_filter']:
        st.session_state['search_term'] = search_txt
        st.session_state['location_filter'] = loc_filter
        st.session_state['search_page'] = 1 # Reset halaman ke-1 jika filter berubah
        st.rerun() # Rerun untuk menerapkan reset page

    # Proses Filter
    filtered_df = df.copy()
    if st.session_state['search_term']:
        filtered_df = filtered_df[
            filtered_df['Posisi'].str.contains(st.session_state['search_term'], case=False, na=False) |
            filtered_df['Perusahaan'].str.contains(st.session_state['search_term'], case=False, na=False)
        ]
    if st.session_state['location_filter'] != "Semua":
        filtered_df = filtered_df[filtered_df['Lokasi'] == st.session_state['location_filter']]

    
    # ==========================
    # 2. PAGINATION LOGIC
    # ==========================
    total_jobs = len(filtered_df)
    
    # Hitung total halaman
    total_pages = math.ceil(total_jobs / JOBS_PER_PAGE)
    
    # Tentukan index awal dan akhir untuk data di halaman ini
    start_index = (current_page_num - 1) * JOBS_PER_PAGE
    end_index = start_index + JOBS_PER_PAGE
    
    # Slicing data
    jobs_to_display = filtered_df.iloc[start_index:end_index]
    jobs_list = jobs_to_display.to_dict('records')
    
    st.subheader(f"Ditemukan {total_jobs} Lowongan (Halaman {current_page_num} dari {total_pages})")

    # ==========================
    # 3. TAMPILAN KARTU (CARD UI)
    # ==========================
    
    # Hitung baris yang dibutuhkan di halaman ini
    num_rows_current_page = math.ceil(len(jobs_list) / COLUMNS_PER_ROW)
    
    
    for row in range(num_rows_current_page):
        # Buat kolom
        cols = st.columns(COLUMNS_PER_ROW)
        
        for col_index in range(COLUMNS_PER_ROW):
            job_index = (row * COLUMNS_PER_ROW) + col_index
            
            if job_index < len(jobs_list):
                job = jobs_list[job_index]
                
                with cols[col_index], st.container(border=True):
                    st.markdown(f"**{job['Perusahaan']}**")
                    st.markdown(f"#### {job['Posisi']}")
                    
                    # Logika Gaji (sama seperti sebelumnya)
                    gaji_min = job['Gaji_Num'] 
                    gaji_max = job['Gaji_Num'] + random.randint(3, 8) 
                    gaji_text = f"**Gaji : Rp{gaji_min} - {gaji_max} Jt/bln**"
                                
                    st.markdown(gaji_text, unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: small; color: gray;'>Lokasi: {job['Lokasi']} | {job['Tanggal Posting']}</p>", unsafe_allow_html=True)
                    
                    st.button("Lihat Detail", key=f"detail_{job['ID']}_{current_page_num}_{job_index}", use_container_width=True)
            else:
                # Kolom kosong
                pass

    st.markdown("---")
    
    # ==========================
    # 4. PAGINATION CONTROLS
    # ==========================
    if total_pages > 1:
        col_prev, col_info, col_next = st.columns([1, 2, 1])

        # Tombol Previous
        if current_page_num > 1:
            if col_prev.button("⬅️ Sebelumnya"):
                st.session_state['search_page'] -= 1
                st.rerun()

        # Tombol Next
        if current_page_num < total_pages:
            if col_next.button("Berikutnya ➡️"):
                st.session_state['search_page'] += 1
                st.rerun()
        
        # Informasi halaman
        col_info.markdown(f"<p style='text-align:center;'>Halaman **{current_page_num}** dari **{total_pages}**</p>", unsafe_allow_html=True)
