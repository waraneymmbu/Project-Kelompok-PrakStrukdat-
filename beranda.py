import streamlit as st
import requests
import html
from datetime import datetime

if "page_configured" not in st.session_state:
    st.set_page_config(
        page_title="Berita Dunia Kerja",
        page_icon="📰",
        layout="wide",
    )
    st.session_state["page_configured"] = True

BASE_URL = "https://saurav.tech/NewsAPI"


def fetch_job_news(limit: int = 60):
    countries = [("id", "Indonesia"), ("us", "USA"), ("gb", "UK")]
    categories = ["business", "general"]

    job_keywords = [
        "job", "jobs", "career", "employment", "recruit", "hiring", "vacancy",
        "salary", "wage", "workers", "layoff", "intern", "apprentice",
        "kerja", "pekerjaan", "lowongan", "loker", "karier",
        "pegawai", "karyawan", "buruh", "phk", "gaji", "upah", "magang",
    ]

    collected = []

    for code, negara in countries:
        for cat in categories:
            url = f"{BASE_URL}/top-headlines/category/{cat}/{code}.json"
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
            except:
                continue

            for a in data.get("articles", []):
                title = a.get("title") or ""
                desc = a.get("description") or ""
                check = (title + " " + desc).lower()

                if not any(k in check for k in job_keywords):
                    continue

                published = a.get("publishedAt")
                waktu = ""
                dt_obj = None

                if published:
                    try:
                        dt_obj = datetime.fromisoformat(published.replace("Z", "+00:00"))
                        waktu = dt_obj.strftime("%d %b %Y %H:%M")
                    except:
                        waktu = published

                collected.append({
                    "judul": html.unescape(title),
                    "ringkasan": html.unescape(desc) if desc else "",
                    "waktu": waktu,
                    "waktu_dt": dt_obj,
                    "sumber": (a.get("source") or {}).get("name", ""),
                    "negara": negara,
                    "url": a.get("url") or "#",
                    "gambar": a.get("urlToImage"),
                })

    unique = {}
    for art in collected:
        if art["url"] not in unique:
            unique[art["url"]] = art

    articles = list(unique.values())
    articles.sort(key=lambda x: x["waktu_dt"] or datetime.min, reverse=True)
    return articles[:limit]

def home_page():

    st.markdown("""
        <style>
        body { background: #f1f5f9; }
        .block-container { max-width: 1100px; padding-top: 1.3rem; }
        
        /* Hero wrapper - HIJAU GELAP */
        .hero-wrapper {
            background: linear-gradient(135deg, #063328 0%, #084032 100%);
            border-radius: 22px; 
            border: 2px solid #0a4a3d;
            padding: 18px 20px 22px 20px; 
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        /* Title - warna putih */
        .hero-title { 
            font-size: 28px; 
            font-weight: 800; 
            color: #ffffff !important;
        }
        
        /* Subtitle - hijau muda */
        .hero-subtitle { 
            font-size: 13px; 
            color: #d1fae5 !important;
            max-width: 650px; 
        }
        
        /* Badge - warna disesuaikan */
        .hero-badge {
            font-size: 11px;
            font-weight: 600;
            color: #ffffff !important;
            background: rgba(13, 92, 77, 0.6) !important;
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            margin-bottom: 6px;
        }
        
        img { border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

    username = st.session_state.get("username", "Cobaaa")

    st.markdown(f"""
        <div class="hero-wrapper">
            <div class="hero-badge">
                Beranda Berita Dunia Kerja
            </div>
            <h1 class="hero-title">Hai, {username}! Cek kabar terbaru dunia kerja & lowongan.</h1>
            <p class="hero-subtitle">
                Di beranda ini kamu bisa lihat berita tentang lowongan, gaji, PHK, tren rekrutmen,
                serikat buruh, dan banyak lagi. Klik judul untuk baca versi lengkap di situs sumber.
            </p>
        </div>
    """, unsafe_allow_html=True)

    articles = fetch_job_news(limit=60)

    st.markdown("Feed Berita Dunia Kerja")
    st.caption("Berita otomatis difilter supaya hanya yang berkaitan dengan pekerjaan & karier.")

    

    if not articles:
        st.info("Belum ada berita yang bisa ditampilkan.")
        return

    cols = st.columns(2)

    for idx, art in enumerate(articles):
        col = cols[idx % 2]
        with col:
            with st.container(border=True):
                if art["gambar"]:
                    try:
                        st.image(art["gambar"], use_container_width=True)
                    except:
                        pass

                meta = " • ".join(
                    p for p in [art["sumber"], art["negara"], art["waktu"]] if p
                )
                st.caption(meta)

                st.markdown(f"**[{art['judul']}]({art['url']})**")

                if art["ringkasan"]:
                    st.write(art["ringkasan"])

                st.write("")

    st.markdown("---")
if __name__ == "__main__":
    home_page()
