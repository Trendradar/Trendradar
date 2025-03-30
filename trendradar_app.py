import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trendradar", layout="wide")

# Seitenmenü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["🧠 Trendradar", "📁 Trend Datenbank", "⭐ Favoriten Trends", "ℹ️ Impressum"])

# CSV einlesen
st.markdown("""<style>code, pre { display: none !important }</style>""", unsafe_allow_html=True)
df = pd.read_csv("trends.csv", encoding="utf-8", sep=",", quotechar='"', dtype=str)
df["Wachstum"] = pd.to_numeric(df["Wachstum"].str.replace(",", ""), errors="coerce")
df["Volumen"] = pd.to_numeric(df["Volumen"].str.replace(",", ""), errors="coerce")

# Funktion zum Zeichnen

def plot_trend(row):
    fig, ax = plt.subplots(figsize=(4, 2))
    views = list(map(int, row["Verlauf"].split(",")))
    ax.plot(range(1, len(views) + 1), views, marker="o")
    ax.set_xticks(range(1, len(views) + 1))
    ax.set_xlabel("Tag")
    ax.set_ylabel("Views")
    ax.set_title("")
    st.pyplot(fig)

# ------------------------
# Hauptseite
# ------------------------

if page == "🧠 Trendradar":

    st.markdown("""
        <h2 style='font-size: 28px; margin-bottom: 20px;'>🔥 Top 3 Trends mit höchstem Wachstum</h2>
    """, unsafe_allow_html=True)

    top3 = df.sort_values("Wachstum", ascending=False).head(3)
    cols = st.columns(3)

    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.markdown(f"""
                <div style='background-color: #f9f9f9; padding: 20px; border-radius: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); margin-bottom: 10px;'>
                    <h3 style='margin: 0 0 8px 0;'>{row['Trend']}</h3>
                    <div style='color: #666; font-size: 14px; margin-bottom: 8px;'>{row['Kategorie']}</div>
                    <div style='color: green; font-weight: bold;'>Wachstum: +{int(row['Wachstum'])}%</div>
                    <div style='color: #2b70ff;'>Volumen: {int(row['Volumen']):,}</div>
                </div>
            """, unsafe_allow_html=True)
            plot_trend(row)

    st.markdown("""<hr style='margin: 40px 0;'>""", unsafe_allow_html=True)

    st.markdown("""
        <h3 style='font-size: 24px; margin-bottom: 20px;'>🌿 Weitere Trends mit starkem Wachstum</h3>
    """, unsafe_allow_html=True)

    remaining = df.sort_values("Wachstum", ascending=False).iloc[3:23]
    rows = [remaining[i:i + 3] for i in range(0, len(remaining), 3)]

    for row_chunk in rows:
        cols = st.columns(3)
        for i, (_, row) in enumerate(row_chunk.iterrows()):
            with cols[i]:
                st.markdown(f"""
                    <div style='background-color: #f9f9f9; padding: 20px; border-radius: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); margin-bottom: 10px;'>
                        <h4 style='margin: 0 0 8px 0;'>{row['Trend']}</h4>
                        <div style='color: #666; font-size: 14px; margin-bottom: 8px;'>{row['Kategorie']}</div>
                        <div style='color: green; font-weight: bold;'>Wachstum: +{int(row['Wachstum'])}%</div>
                        <div style='color: #2b70ff;'>Volumen: {int(row['Volumen']):,}</div>
                    </div>
                """, unsafe_allow_html=True)
                plot_trend(row)