import streamlit as st
import time
import traceback
from database import get_user_profile, update_user_profile

def local_css():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .page-header {
            font-size: 28px;
            font-weight: 700;
            color: #1b7c3a;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.3rem;
        }

        .page-subtitle {
            font-size: 14px;
            color: #4a5568;
            margin-bottom: 1rem;
        }

        .pill {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 999px;
            background-color: #e6fffa;
            color: #047857;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .header-bar {
            background: #0f172a;
            border-radius: 999px;
            padding: 10px 18px;
            color: #e5e7eb;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 6px 14px rgba(15, 23, 42, 0.35);
            margin-bottom: 10px;
        }

        .header-bar-icon {
            font-size: 18px;
        }

        .header-bar-text {
            font-size: 14px;
            font-weight: 600;
        }

        [data-testid="stFileUploaderDropzone"] small {
            display: none !important;
        }

        .avatar-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            margin-top: 4px;
            margin-bottom: 8px;
        }

        .avatar-img {
            border-radius: 50%;
            border: 3px solid #e5e7eb;
            padding: 4px;
        }

        .username-badge {
            font-weight: 600;
            font-size: 14px;
            color: #111827;
        }

        .username-caption {
            font-size: 11px;
            color: #6b7280;
        }

        .section-title {
            font-size: 15px;
            font-weight: 700;
            color: #111827;
            margin-bottom: 2px;
        }

        .section-caption {
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 6px;
        }

        .cv-box {
            border: 1px dashed #4CAF50;
            padding: 14px;
            border-radius: 10px;
            background-color: #f5fffa;
            text-align: left;
        }

        .status-badge-ok {
            display: inline-block;
            padding: 3px 9px;
            border-radius: 999px;
            background-color: #dcfce7;
            color: #166534;
            font-size: 11px;
            font-weight: 600;
        }

        .status-badge-empty {
            display: inline-block;
            padding: 3px 9px;
            border-radius: 999px;
            background-color: #fee2e2;
            color: #991b1b;
            font-size: 11px;
            font-weight: 600;
        }

        .stButton > button {
            border-radius: 999px !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def profile_page():
    local_css()

    if "username" not in st.session_state:
        st.session_state["username"] = "user_demo"
    username = st.session_state["username"]

    st.markdown(
        "<div class='page-header'>👤 Profil & Dokumen Saya</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='page-subtitle'>Kelola informasi pribadi, CV, portofolio, dan tautan LinkedIn Anda.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<span class='pill'>Account</span>", unsafe_allow_html=True)
    st.write("")

    try:
        user_data = get_user_profile(username)
    except Exception:
        print("Error get_user_profile:\n", traceback.format_exc())
        user_data = None

    if user_data and len(user_data) >= 9:
        (
            db_email,
            db_fullname,
            db_age,
            db_about,
            db_history,
            db_photo,
            db_cv,
            db_linkedin,
            db_portfolio,
        ) = user_data[0:9]
    else:
        db_email = ""
        db_fullname = ""
        db_age = 18
        db_about = ""
        db_history = ""
        db_photo = None
        db_cv = None
        db_linkedin = ""
        db_portfolio = None

    if "cv_bytes" not in st.session_state:
        st.session_state["cv_bytes"] = db_cv
    if "portfolio_bytes" not in st.session_state:
        st.session_state["portfolio_bytes"] = db_portfolio

    current_cv_bytes = st.session_state["cv_bytes"]
    current_portfolio_bytes = st.session_state["portfolio_bytes"]

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="header-bar">
                <span class="header-bar-icon">📸</span>
                <span class="header-bar-text">Foto & Akun</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="avatar-wrapper">
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                     width="140"
                     class="avatar-img">
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"<div class='username-badge'>@{username}</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='username-caption'>Avatar default digunakan sebagai foto profil.</div>",
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Keluar"):
            st.session_state['logged_in'] = False
            st.session_state['current_page'] = 'Home'
            st.session_state['profile_pic_preview'] = None
            st.session_state['search_page'] = 1
            st.session_state['search_term'] = ""
            st.session_state['location_filter'] = "Semua"
            st.rerun()

        st.markdown(
            """
            <div class="header-bar">
                <span class="header-bar-icon">📝</span>
                <span class="header-bar-text">Informasi Pribadi</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("form_profil_lengkap", border=False):
            st.markdown(
                "<div class='section-caption'>Isi data di bawah ini dengan benar untuk memperkuat profil Anda.</div>",
                unsafe_allow_html=True,
            )

            c_nama, c_umur = st.columns([3, 1])
            with c_nama:
                fname_inp = st.text_input("Nama Lengkap", value=db_fullname)
            with c_umur:
                age_val = int(db_age) if str(db_age).isdigit() else 18
                age_inp = st.number_input("Umur", 17, 70, age_val)

            email_inp = st.text_input("Email", value=db_email)
            about_inp = st.text_area("Tentang Saya", value=db_about, height=80)
            history_inp = st.text_area("Riwayat Pekerjaan", value=db_history, height=100)

            st.markdown("<hr>", unsafe_allow_html=True)

            linkedin_inp = st.text_input("URL Profil LinkedIn", value=db_linkedin)

            uploaded_cv_file = st.file_uploader("Upload CV", type=["pdf", "docx"])
            if uploaded_cv_file:
                st.session_state["cv_bytes"] = uploaded_cv_file.read()
                st.success("CV siap disimpan.")

            uploaded_portfolio = st.file_uploader("Upload Portofolio", type=["pdf", "ppt", "zip"])
            if uploaded_portfolio:
                st.session_state["portfolio_bytes"] = uploaded_portfolio.read()
                st.success("Portofolio siap disimpan.")

            tombol_simpan = st.form_submit_button("💾 Simpan Semua Perubahan")

            if tombol_simpan:
                st.info("Sedang memproses penyimpanan...")
                try:
                    success = update_user_profile(
                        username,
                        fname_inp,
                        age_inp,
                        about_inp,
                        history_inp,
                        email_inp,
                        linkedin_inp,
                        db_photo,
                        current_cv_bytes,
                        current_portfolio_bytes,
                    )

                    if success:
                        st.success("Profil berhasil diperbarui.")
                        time.sleep(1)
                    else:
                        st.error("Gagal menyimpan data.")
                except Exception:
                    st.error("Terjadi kesalahan sistem.")
                    st.text(traceback.format_exc())
