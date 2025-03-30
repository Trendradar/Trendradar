import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trendradar", layout="wide")

# Seitenmenü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["ℹ️ Trendradar", "📁 Trend Datenbank", "⭐ Favoriten Trends", "📘 Impressum"])

# CSV laden
@st.cache_data
def load_data():
    df = pd.read_csv("trends.csv", encoding="utf-8", sep=",", quotechar='"')
    df["Wachstum"] = pd.to_numeric(df["Wachstum"].str.replace(",", ""), errors="coerce")
    df["Volumen"] = pd.to_numeric(df["Volumen"].str.replace(",", ""), errors="coerce")
    return df

df = load_data()

# Chart zeichnen
def plot_trend(row):
    fig, ax = plt.subplots(figsize=(4, 2))
    views = list(map(int, row["Verlauf"].split(",")))
    ax.plot(range(1, len(views)+1), views, marker="o")
    ax.set_title("")
    ax.set_xlabel("Tag")
    ax.set_ylabel("Views")
    st.pyplot(fig)

# Trendkarte zeichnen
def draw_trend_card(row):
    with st.container():
        st.markdown(
            f"""
            <div style='padding: 1rem; border-radius: 1rem; background-color: #f9f9f9; box-shadow: 0 2px 8px rgba(0,0,0,0.06);'>
                <div style='font-size: 1.25rem; font-weight: bold;'>{row['Trend']}</div>
                <div style='color: grey; margin-bottom: 0.5rem;'>{row['Kategorie']}</div>
                <div style='color: green; font-weight: bold;'>Wachstum: +{row['Wachstum']}%</div>
                <div style='color: #007bff;'>Volumen: {int(row['Volumen']):,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        plot_trend(row)

# Hauptseite
if page == "ℹ️ Trendradar":
    st.markdown("<h2 style='margin-bottom: 2rem;'>🔥 Top 3 Trends mit höchstem Wachstum</h2>", unsafe_allow_html=True)
    top3 = df.sort_values("Wachstum", ascending=False).head(3)
    cols = st.columns(3)
    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            draw_trend_card(row)

    st.markdown("<hr style='margin: 3rem 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-bottom: 2rem;'>📉 Weitere Trends mit starkem Wachstum</h3>", unsafe_allow_html=True)
    remaining = df.sort_values("Wachstum", ascending=False).dropna().iloc[3:23]
    cols = st.columns(3)
    for i, (_, row) in enumerate(remaining.iterrows()):
        with cols[i % 3]:
            draw_trend_card(row)
