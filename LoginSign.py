import streamlit as st

if 'page_state' not in st.session_state:
    st.session_state.page_state = 'login'

st.markdown("""
    <style>
    .form_submit_button {
        background-color: green;
    }
    </style>
""", unsafe_allow_html=True)


def login_page_pure_python():
    """
    Menampilkan halaman login GetCareer.
    """
    
    st.set_page_config(
        page_title="GetCareer - Masuk",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.title("Get:green[Career]") 
    st.subheader("Temukan peluang karir Anda berikutnya.")
    st.divider()

    if st.session_state.page_state == 'login':
        display_login_form()
    elif st.session_state.page_state == 'forgot_password':
        display_forgot_password_form()
    elif st.session_state.page_state == 'sign_in':
        sign_in()

def display_login_form():
    """
    Menampilkan formulir login dan tombol Lupa Kata Sandi.
    """
    
    with st.container(border=False):
        st.header("Masuk ke Akun Anda")

        with st.form(key='login_form'):
            
            credential = st.text_input(
                "Email/Username", 
                placeholder="Masukkan alamat email atau username Anda"
            )

            password = st.text_input(
                "Kata Sandi", 
                type="password", 
                placeholder="Masukkan kata sandi"
            )
            
            login_button = st.form_submit_button(
                "Masuk ke Akun", 
                type="primary",
                use_container_width=True
            ) 

            if login_button:
                if (credential.lower() == "admin" or credential.lower() == "user@example.com") and password == "12345":
                    st.success("Login Berhasil! Selamat datang.")
                    st.balloons()
                else:
                    st.error("Email/Username atau Kata Sandi salah.")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Lupa Kata Sandi?", key="forgot_pass_btn"):
            st.session_state.page_state = 'forgot_password'
            st.rerun()

    with col2:
        if st.button("Daftar Akun Baru", key="signup_btn"):
            st.session_state.page_state = 'sign_in'
            st.rerun()


def display_forgot_password_form():
    """
    Menampilkan formulir untuk fitur Forgot Password.
    """
    st.header("Lupa Kata Sandi")
    
    with st.container(border=True):
        st.write("Masukkan email yang terdaftar untuk menerima tautan reset kata sandi.")
        
        with st.form(key='forgot_password_form'):
            reset_email = st.text_input(
                "Email Terdaftar", 
                placeholder="misalnya: user@example.com"
            )
            
            send_link_button = st.form_submit_button(
                "Kirim Tautan Reset", 
                type="primary", 
                use_container_width=True
            )
            
            if send_link_button:
                if "@" in reset_email and "." in reset_email:
                    st.success(f"Tautan reset telah dikirim ke **{reset_email}**. Cek email Anda!")
                else:
                    st.error("Masukkan alamat email yang valid.")

        st.divider()
        if st.button("⬅Kembali ke Halaman Login", key='back_to_login_btn'):
            st.session_state.page_state = 'login'
            st.rerun()

def sign_in():
    """
    Menampilkan halaman Sign In/Login untuk aplikasi GetCareer.
    """
    
    st.title("Sign Up") 
    
    with st.form(key='login_form'):
        username = st.text_input("Username", placeholder="Masukkan Username Anda")
        
        password = st.text_input("Password", type="password", placeholder="Masukkan Password Anda")
        
        sign_in_button = st.form_submit_button("Sign Up")

        # if sign_in_button:
        #     if username == "admin" and password == "adminpass":
        #         st.success("Login Berhasil! Selamat datang admin.")
        #     else:
        #         st.error("Username atau Password salah.")
    if st.button("⬅Kembali ke Halaman Login", key='back_to_login_btn'):
        st.session_state.page_state = 'login'
        st.rerun()
    st.markdown("---") 

if __name__ == "__main__":
    login_page_pure_python()
