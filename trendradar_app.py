import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trendradar", layout="wide")

# Seitenmenü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["📊 Trendradar", "📁 Trend Datenbank", "⭐ Favoriten Trends", "ℹ️ Impressum"])

# CSV laden
@st.cache_data
def load_data():
    df = pd.read_csv("trends.csv", encoding="utf-8", sep=",", quotechar='"')
    df["Wachstum"] = pd.to_numeric(df["Wachstum"], errors="coerce")
    df["Volumen"] = pd.to_numeric(df["Volumen"].astype(str).str.replace(",", ""), errors="coerce")
    return df.dropna()

df = load_data()

# Funktion: Trend-Chart zeichnen
def plot_trend(row):
    fig, ax = plt.subplots(figsize=(4, 2))
    views = list(map(int, str(row["Verlauf"]).split(",")))
    ax.plot(range(1, len(views)+1), views, marker="o")
    ax.set_title("")
    ax.set_xlabel("Tag")
    ax.set_ylabel("Views")
    st.pyplot(fig)

# Hauptseite
if page == "📊 Trendradar":
    st.markdown("""
        <h2 style='font-size: 28px;'>🔥 Top 3 Trends mit höchstem Wachstum</h2>
    """, unsafe_allow_html=True)

    top3 = df.sort_values("Wachstum", ascending=False).head(3)
    cols = st.columns(3)

    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.markdown(f"""
                <div style='background-color: #f9f9f9; padding: 20px; border-radius: 15px; box-shadow: 0px 0px 4px rgba(0,0,0,0.05);'>
                    <h4 style='margin-bottom: 0.3rem;'>{row['Trend']}</h4>
                    <div style='color: grey; margin-bottom: 0.2rem;'>{row['Kategorie']}</div>
                    <div style='color: green; font-weight: bold;'>Wachstum: +{int(row['Wachstum'])}%</div>
                    <div style='color: #3399ff;'>Volumen: {int(row['Volumen']):,}</div>
            """, unsafe_allow_html=True)
            plot_trend(row)
            st.markdown("""</div>""", unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown("""
        <h3 style='font-size: 24px;'>📈 Weitere Trends mit starkem Wachstum</h3>
    """, unsafe_allow_html=True)

    remaining = df.sort_values("Wachstum", ascending=False).iloc[3:23]  # Platz 4-24
    cols = st.columns(3)

    for i, (_, row) in enumerate(remaining.iterrows()):
        with cols[i % 3]:
            st.markdown(f"""
                <div style='background-color: #f9f9f9; padding: 20px; border-radius: 15px; box-shadow: 0px 0px 4px rgba(0,0,0,0.05);'>
                    <h5 style='margin-bottom: 0.3rem;'>{row['Trend']}</h5>
                    <div style='color: grey; margin-bottom: 0.2rem;'>{row['Kategorie']}</div>
                    <div style='color: green; font-weight: bold;'>Wachstum: +{int(row['Wachstum'])}%</div>
                    <div style='color: #3399ff;'>Volumen: {int(row['Volumen']):,}</div>
            """, unsafe_allow_html=True)
            plot_trend(row)
            st.markdown("""</div>""", unsafe_allow_html=True)
