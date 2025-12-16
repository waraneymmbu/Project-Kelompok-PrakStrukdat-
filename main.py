import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from database import get_db_connection
from LoginSign import auth_page
from beranda import home_page
from pencarian import search_jobs_page
from profile import profile_page
from map import map
from ai import ai_consultation_page
from jobcomparassion import job_comp_page
from interview import interview_page


st.set_page_config(
    page_title="Getcareer - Platform Karier Terbaik",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: linear-gradient(135deg, #0d5c4d 0%, #1a4038 100%);
        padding: 1rem 3rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: space-between; /* Pisahkan tabs dan logo */
        align-items: center;
    }
    
    /* Tambahkan logo GetCareer di kanan */
    .stTabs [data-baseweb="tab-list"]::after {
        content: "GetCareer";
        color: white;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-left: auto;
        padding-left: 2rem;
    }
    
    /* Tab buttons styling */
    .stTabs [data-baseweb="tab-list"] button {
        color: white !important;
        font-weight: 500;
    }
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
    .stTabs [data-baseweb="tab-list"] {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: linear-gradient(135deg, #0d5c4d 0%, #1a4038 100%);
        padding: 1rem 3rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: center;
        gap: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        color: white !important;
        font-size: 20px !important;
        padding: 14px 26px !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
        min-width: 55px;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: rgba(255, 255, 255, 0.18) !important;
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.25) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.4) !important;
        transform: scale(1.1);
    }
    
    .main .block-container {
        padding-top: 9rem !important;
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* Hide text, show only icons */
    .stTabs [data-baseweb="tab-list"] button {
        font-family: "Font Awesome 6 Free" !important;
    }


    /* Input fields dengan gradient */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: linear-gradient(135deg, #15866d 0%, #1a9b7f 100%) !important;
        color: white !important;
        border: 2px solid #1a9b7f !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    /* Button dengan gradient */
    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {
        background: linear-gradient(135deg, #0d5c4d 0%, #0a4a3d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #0a4a3d 0%, #083829 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(13, 92, 77, 0.4);
    }
    /* Membuat tabs navbar fixed di atas */
    .stTabs [data-baseweb="tab-list"] {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background-color: #0d5c4d;
        padding: 1rem 3rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* PENTING: Memberikan padding di konten agar tidak tertutup navbar */
    .main .block-container {
        padding-top: 8rem !important;  /* Tingkatkan dari 5rem ke 8rem */
        padding-bottom: 2rem;
    }
    
    /* Padding untuk tab content */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem;
    }
    
    /* Sembunyikan sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Hilangkan header termasuk tombol Deploy */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* Background */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.7)), 
                    url("https://i.pinimg.com/1200x/b2/63/84/b2638436ebd939dccce6f329136a16c9.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Styling lainnya */
    .main-header {
        font-size: 2.5rem; 
        color: #00B14F; 
        font-weight: 700;
    }
    
    .stButton>button {
        background-color: #00B14F;
        color: white;
        border-radius: 8px; 
        font-weight: bold;
        padding: 10px;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #008f40; 
        color: white;
    }
    
    .stContainer {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .centered-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    .big-icon { 
        font-size: 80px; 
        color: #00B14F; 
        margin-bottom: 20px; 
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    defaults = {
        'logged_in': False,
        'user_role': None,
        'username': "",
        'auth_mode': 'login', 
        'current_page': 'Home',
        'profile_pic_preview': None,
        'search_page': 1
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

@st.cache_data
def get_jobs():
    """Menghasilkan DataFrame data lowongan kerja dummy."""
    data = []
    companies = ['Gojek', 'Tokopedia', 'Shopee', 'Traveloka', 'Grab', 'Bank BCA', 'Pertamina', 'Telkomsel']
    roles = ['Data Analyst', 'Software Engineer', 'Product Manager', 'UI/UX Designer', 'Digital Marketing', 'HR Manager']
    
    for i in range(30):
        gaji_int = random.randint(6, 35) # Gaji dalam juta
        data.append({
            "ID": i + 1,
            "Posisi": random.choice(roles),
            "Perusahaan": random.choice(companies),
            "Gaji_Num": gaji_int,
            "Lokasi": random.choice(['Jakarta', 'Remote', 'Bandung', 'Surabaya', 'Bali']),
            "Tanggal Posting": (datetime.now() - timedelta(days=random.randint(1, 20))).strftime("%Y-%m-%d")
        })
    return pd.DataFrame(data)


def main():
    """Fungsi utama yang mengontrol alur aplikasi."""
    if st.session_state['logged_in']:
        st.sidebar.title("Menu")
        
        if st.session_state['user_role'] == 'admin':
            st.sidebar.warning("🔧 Mode Admin")
            page = st.sidebar.selectbox("Pilih Halaman", ["Beranda", "Database User"])
            
            if page == "Beranda": 
                home_page()
            elif page == "Database User": 
                st.title("Database Pengguna")
                st.dataframe(pd.read_sql("SELECT * FROM userdata", get_db_connection()), use_container_width=True)
            
                
        else:
            menu_dict = {"Home": "Beranda", "SearchJobs": "Cari Kerja", "Profile": "Profile", "MapJobs": "Map", "AIConsult": "Konsultasi AI", "AIJob": "Job Comparassion", "AIInterview":"Interview Pertanyaan"}
            selected = st.sidebar.radio("Ke Halaman:", list(menu_dict.keys()), format_func=lambda x: menu_dict[x])
            st.session_state['current_page'] = selected
            st.sidebar.markdown("---")
            

            # if st.session_state['current_page'] == 'Home': 
            #     home_page()
            # elif st.session_state['current_page'] == 'SearchJobs': 
            #     search_jobs_page(get_jobs, st.session_state['search_page'])
            # elif st.session_state['current_page'] == 'Profile': 
            #     profile_page()
            # elif st.session_state['current_page'] == 'MapJobs':
            #     map()
            # elif st.session_state['current_page'] == 'AIConsult':
            #     ai_consultation_page(get_jobs)
            # elif st.session_state['current_page'] == 'AIJob':
            #     job_comp_page(get_jobs)
            # elif st.session_state['current_page'] == 'AIInterview':
            #     interview_page(get_jobs)
            if 'current_page' not in st.session_state:
                st.session_state['current_page'] = 'Home'

            # Buat tabs
            # tabs = st.tabs(["🏠 ", "💼", "👤", "🗺️", 
            #                 "🤖", "📊", "🎤"])

            tabs = st.tabs(["Home", "Search", "Profile", "Map", "AI", "Compare", "Interview"])

            # Tab 1 - Home
            with tabs[0]:
                st.session_state['current_page'] = 'Home'
                home_page()

            # Tab 2 - Search Jobs
            with tabs[1]:
                st.session_state['current_page'] = 'SearchJobs'
                search_jobs_page(get_jobs, st.session_state.get('search_page', 1))

            # Tab 3 - Profile
            with tabs[2]:
                st.session_state['current_page'] = 'Profile'
                profile_page()

            # Tab 4 - Map
            with tabs[3]:
                st.session_state['current_page'] = 'MapJobs'
                map()

            # Tab 5 - AI Consult
            with tabs[4]:
                st.session_state['current_page'] = 'AIConsult'
                ai_consultation_page()

            # Tab 6 - Job Comparison
            with tabs[5]:
                st.session_state['current_page'] = 'AIJob'
                job_comp_page()

            # Tab 7 - Interview
            with tabs[6]:
                st.session_state['current_page'] = 'AIInterview'
                interview_page()
    else:
        auth_page()
    # Inisialisasi
# tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
#     "🏠 Beranda", 
#     "💼 Cari Kerja", 
#     "👤 Profile", 
#     "🗺️ Map", 
#     "🤖 Konsultasi AI",
#     "📊 Job Comparassion",
#     "💬 Interview"
# ])

# with tab2:
#     st.title("Cari Lowongan Kerja")
#     # konten cari kerja...
if __name__ == '__main__':
    main()
