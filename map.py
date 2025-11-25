import streamlit as st
import pandas as pd
import pydeck as pdk

CITY_COORDS = {
    "Jakarta": (-6.2088, 106.8456),
    "Bandung": (-6.9175, 107.6191),
    "Surabaya": (-7.2575, 112.7521),
    "Bali": (-8.3405, 115.0920),
    "Remote": (0, 0)
}

def map(get_jobs):
    st.title("Pekerjaan Terdekat")

    df = get_jobs()

    df['lat'] = df['Lokasi'].map(lambda x: CITY_COORDS.get(x, (0,0))[0])
    df['lon'] = df['Lokasi'].map(lambda x: CITY_COORDS.get(x, (0,0))[1])

    location_filter = st.selectbox("Filter lokasi:", ["Semua"] + list(CITY_COORDS.keys()))
    if location_filter != "Semua":
        df = df[df['Lokasi'] == location_filter]

    if df.empty:
        st.info("Tidak ada pekerjaan di lokasi ini.")
        return
    st.subheader("Peta Lokasi Pekerjaan")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=df['lat'].mean(),
            longitude=df['lon'].mean(),
            zoom=5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[lon, lat]',
                get_fill_color='[0, 180, 0, 160]',
                get_radius=50000,
                pickable=True
            )
        ],
        tooltip={"text": "{Posisi}\n{Perusahaan}\n{Lokasi}"}
    ))

