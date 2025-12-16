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


def job_comp_page():

    st.title("Job Comparassion")

    st.write("""
    Masukkan dua pekerjaan yang ingin kamu bandingkan.
    """)

    with st.form("job_form3"):
        satu = st.text_input("Tuliskan Pekerjaan Pertama")
        dua = st.text_input("Tuliskan Pekerjaan Kedua")

        submit = st.form_submit_button("Cari Tahu")

    if not submit:
        return

    # if not satu.strip():
    #     st.warning("Isi minimal bagian *pekerjaan* dulu.")
    #     return

    prompt = f"""
Bandingkan Kedua pekerjaan ini: {satu} dengan {dua}

berikan
1. kelebihan dan kekurang keduanya
2. rata rata gaji keduanya
3. demand pekerjaan keduanya
4. perbandingan ketersediaan kedua pekerjaan
* catatan bagilah setiap point menggunakan pembatas
"""

    jawaban = ask_groq(prompt)

    st.subheader("Rekomendasi AI")
    st.write(jawaban)
