import streamlit as st
import requests

API_KEY = "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"  

def map():


    st.set_page_config(layout="wide")
    st.title("Peta Global Ketersediaan Pekerjaan")

    st.markdown("""
    Visualisasi ini menunjukkan distribusi employment di berbagai negara di dunia.
    """)

    st.components.v1.iframe(
        "https://ourworldindata.org/grapher/employment-to-population-ratio?tab=map",
        height=600,
        scrolling=True
    )
    

    # st.title("Konsultasi AI: Temukan Pekerjaan Cocok untukmu")

    st.write("""
    Masukkan Nama Negara Untuk Refrensi Job yang diminati di negara tersebut.
    """)

    with st.form("job_form"):
        negara = st.text_input("Nama Negara")
        # bakat = st.text_input("Bakat/keterampilanmu:")
        # kepribadian = st.text_input("Kepribadian (introvert/ekstrovert/dll):")
        # hobi = st.text_input("Hobi paling sering dilakukan:")
        # tujuan = st.text_input("Tujuan karier (gaji besar, fleksibel, kreatif, dll):")

        submit = st.form_submit_button("Submit")

    if not submit:
        return

    # if not negara.strip():
    #     st.warning("Isi minimal bagian *minat* dulu.")
    #     return

    prompt = f"""
carikan data pekerjaan paling diminati dari negara berikut:

negara: {negara}

Berikan:
1. list pekerjaan-pekerjaan yang diminati dinegara tersebut
"""

    jawaban = ask_groq(prompt)

    # st.subheader("Rekomendasi AI")
    st.write(jawaban)


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


# def test(get_jobs):

    
