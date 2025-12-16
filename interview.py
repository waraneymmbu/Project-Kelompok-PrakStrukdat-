import streamlit as st
import requests

API_KEY = "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"  


def ask_groq(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    try:
        res = requests.post(url, headers=headers, json=data, timeout=30)
    except requests.RequestException as e:
        return f"Gagal menghubungi API: {e}"

    if res.status_code != 200:
        return f"API Error ({res.status_code}): {res.text}"

    j = res.json()
    return j["choices"][0]["message"]["content"]


def interview_page():

    st.title("Temukan Jawaban Agar Bisa Lolos Interview!")

    st.write("""
    Masukkan pekerjaanmu.
    """)

    with st.form("job_form2"):
        pekerjaan = st.text_input("Tuliskan Pekerjaanmu")

        submit = st.form_submit_button("Dapatkan Pertanyaan Interviewer")

    if not submit:
        return

    if not pekerjaan.strip():
        st.warning("Isi minimal bagian *pekerjaan* dulu.")
        return

    prompt = f"""
Tampilkan pertanyaan-pertanyaan interview pekerjaan {pekerjaan}

Berikan:
1. 10 pertanyaan interviewer yang paling sering keluar
2. Tips diterima kerja dibidang ini
3. Kelebihan & kekurangannya 
"""

    jawaban = ask_groq(prompt)

    # st.subheader("Rekomendasi AI")
    st.write(jawaban)
