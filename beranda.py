import streamlit as st

def home_page():
    """Halaman Beranda untuk pengguna yang sudah login."""
    st.markdown(f"<h1 class='main-header'>Halo, {st.session_state['username']}! 👋</h1>", unsafe_allow_html=True)
    st.write("Temukan pekerjaan impianmu hari ini.")
    
    # Metrik
    c1, c2, c3 = st.columns(3)
    c1.metric("Lowongan Aktif", "1,250+", "24 Hari ini")
    c2.metric("Perusahaan", "500+", "Partner Resmi")
    c3.metric("Pencari Kerja", "15k", "Aktif")

    st.markdown("---")
    
    # Navigasi cepat
    col_a, col_b = st.columns(2)
    if col_a.button("🔍 Cari Lowongan Kerja", use_container_width=True):
        st.session_state['current_page'] = 'SearchJobs'
        st.rerun()
    if col_b.button("👤 Update Profil", use_container_width=True):
        st.session_state['current_page'] = 'Profile'
        st.rerun()
