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


def ai_consultation_page():

    st.title("Konsultasi AI: Temukan Pekerjaan Cocok untukmu")

    st.write("""
    Masukkan preferensi dan data dirimu. AI akan memberikan rekomendasi pekerjaan yang paling cocok.
    """)

    with st.form("job_form1"):
        minat = st.text_input("Minat (contoh: desain, game, coding):")
        bakat = st.text_input("Bakat/keterampilanmu:")
        kepribadian = st.text_input("Kepribadian (introvert/ekstrovert/dll):")
        hobi = st.text_input("Hobi paling sering dilakukan:")
        tujuan = st.text_input("Tujuan karier (gaji besar, fleksibel, kreatif, dll):")

        submit = st.form_submit_button("Dapatkan Rekomendasi AI")

    if not submit:
        return

    if not minat.strip():
        st.warning("Isi minimal bagian *minat* dulu.")
        return

    prompt = f"""
Buatkan rekomendasi pekerjaan berdasarkan data berikut:

Minat: {minat}
Bakat: {bakat}
Kepribadian: {kepribadian}
Hobi: {hobi}
Tujuan Karier: {tujuan}

Berikan:
1. 3 rekomendasi pekerjaan paling cocok
2. Alasan singkat
3. Kelebihan & kekurangannya bagi user
4. Skill yang harus ditingkatkan
"""

    jawaban = ask_groq(prompt)

    st.subheader("Rekomendasi AI")
    st.write(jawaban)
