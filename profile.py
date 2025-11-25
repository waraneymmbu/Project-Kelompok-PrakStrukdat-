import streamlit as st
import time 
import io
from database import get_user_profile, update_user_profile

def profile_page():
    """Halaman profil pengguna untuk update data."""
    st.title("Profil Saya")
    
    user_data = get_user_profile(st.session_state['username'])
    if user_data:
        db_email, db_fullname, db_age, db_about, db_history = user_data
    else:
        db_email, db_fullname, db_age, db_about, db_history = ("", "", 0, "", "")

    col_left, col_right = st.columns([1, 2], gap="large")
    
    with col_left:
        with st.container(border=True):
            st.markdown("<h4 style='text-align:center;'>Foto Profil</h4>", unsafe_allow_html=True)
            
            if st.session_state['profile_pic_preview'] and isinstance(st.session_state['profile_pic_preview'], io.BytesIO):
                st.image(st.session_state['profile_pic_preview'], width=200, use_container_width=True)
            else:
                st.markdown("""
                    <div style="display:flex; justify-content:center; margin-bottom:15px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/4140/4140048.png" width="150" style="border-radius:50%; border: 4px solid #00B14F;">
                    </div>
                """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Ganti Foto", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")
            if uploaded_file is not None:
                st.session_state['profile_pic_preview'] = io.BytesIO(uploaded_file.read())
                st.toast("Foto berhasil diunggah!")
                time.sleep(1)
                st.rerun()
                
            st.markdown("---")
            st.write(f"**Username:** @{st.session_state['username']}")
            st.write(f"**Status:** Job Seeker")

    with col_right:
        with st.form("profile_update_form"):
            st.markdown("### Informasi Pribadi")
            
            c_name, c_age = st.columns([3, 1])
            with c_name:
                full_name_inp = st.text_input("Nama Lengkap", value=db_fullname if db_fullname else "")
            with c_age:
                age_inp = st.number_input("Umur", min_value=17, max_value=70, value=db_age if db_age else 18)
            
            email_inp = st.text_input("Alamat E-mail", value=db_email if db_email else "")

            st.markdown("### Tentang Saya (About Me)")
            about_inp = st.text_area("Deskripsi Singkat", value=db_about if db_about else "", height=100)

            st.markdown("### Riwayat Pekerjaan")
            history_inp = st.text_area("Pengalaman Kerja", value=db_history if db_history else "", height=150)
            
            save_btn = st.form_submit_button("Simpan Perubahan", type="primary")
            if save_btn:
                if update_user_profile(st.session_state['username'], full_name_inp, age_inp, about_inp, history_inp, email_inp):
                    st.success("Data Profil berhasil disimpan!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Gagal menyimpan data.")
