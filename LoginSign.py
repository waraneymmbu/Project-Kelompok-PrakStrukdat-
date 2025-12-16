import streamlit as st
import time 
from database import make_hashes, login_user_db, register_user

def auth_page():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="centered-content">
            <span class="big-icon">💼</span> 
            <h1 style='color:white; text-align: center;'>Getcareer</h1>
            <p style='text-align: center;'>Bangun Masa Depan Kariermu Di Sini</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            if st.session_state['auth_mode'] == 'login':
                st.subheader("Login ke Akun anda")
                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type='password')
                    submitted = st.form_submit_button("Log-In")

                    if submitted:
                        hashed_pswd = make_hashes(password)
                        result = login_user_db(username, hashed_pswd)
                        
                        if result:
                            st.session_state['logged_in'] = True
                            st.session_state['username'] = username
                            st.session_state['user_role'] = result[0][3] # role
                            st.success("Login Berhasil!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Username atau Password salah")

                st.markdown("---")

                st.write("Belum punya akun?")
                if st.button("Buat Akun"):
                    st.session_state['auth_mode'] = 'register'
                    st.rerun()

            elif st.session_state['auth_mode'] == 'register':
                st.subheader("Buat Akun Baru")
                st.info("Lengkapi data berikut untuk mendaftar.")
                
                with st.form("register_form"):
                    new_user = st.text_input("Username *", placeholder="Buat username Anda")
                    new_email = st.text_input("Alamat E-mail *", placeholder="contoh: strukdat@gmail.com")
                    new_password = st.text_input("Password *", type='password', placeholder="Buat password Anda")
                    confirm_password = st.text_input("Retype Password *", type='password', placeholder="Ketik ulang password")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    submitted = st.form_submit_button("Buat Akun")

                    if submitted:
                        if not new_user or not new_email or not new_password:
                            st.warning("Semua kolom bertanda (*) wajib diisi.")
                        elif new_password != confirm_password:
                            st.error("Password tidak sama!")
                        elif len(new_password) < 4:
                            st.warning("Password minimal 4 karakter.")
                        elif "@" not in new_email:
                            st.warning("Format E-mail tidak valid.")
                        else:
                            hashed_pw = make_hashes(new_password)
                            if register_user(new_user, new_email, hashed_pw):
                                st.success("Akun berhasil dibuat! Silakan Login.")
                                time.sleep(1.5)
                                st.session_state['auth_mode'] = 'login' 
                                st.rerun()
                            else:
                                st.error("Username sudah digunakan. Atau E-mail sudah terdaftar.")
                
                st.markdown("---")
                if st.button("Kembali ke halaman Log-In"):
                    st.session_state['auth_mode'] = 'login'
                    st.rerun()
