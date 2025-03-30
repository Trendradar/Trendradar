import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Seiteneinstellungen
st.set_page_config(page_title="Trendradar", layout="wide")

# Fix: Seitenende nicht abschneiden
st.markdown("""
    <style>
    .block-container {
        padding-bottom: 500px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Seitenmenü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["ℹ️ Trendradar", "📂 Trend Datenbank", "⭐ Favoriten Trends", "📄 Impressum"])

# CSV laden
df = pd.read_csv("trends.csv", encoding="utf-8", sep=",", quotechar='"', engine="python")

# Spalten umwandeln
df["Wachstum"] = pd.to_numeric(df["Wachstum"], errors="coerce")
df["Volumen"] = pd.to_numeric(df["Volumen"].astype(str).str.replace(",", ""), errors="coerce")

# Chartfunktion
def plot_trend(row):
    fig, ax = plt.subplots(figsize=(4, 2))
    views = list(map(int, row["Verlauf"].split(",")))
    ax.plot(range(1, len(views) + 1), views, marker="o")
    ax.set_title("")
    ax.set_xlabel("Tag")
    ax.set_ylabel("Views")
    st.pyplot(fig)

# Hauptseite
if page == "ℹ️ Trendradar":
    st.markdown("## 🔥 Top 3 Trends mit höchstem Wachstum")
    top3 = df.sort_values("Wachstum", ascending=False).head(3)
    cols = st.columns(3)

    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.markdown(f"### {row['Trend']}")
            st.caption(row["Kategorie"])
            st.markdown(f"**<span style='color:green'>Wachstum: +{row['Wachstum']}%</span>**", unsafe_allow_html=True)
            st.markdown(f"**<span style='color:#3999ff'>Volumen: {int(row['Volumen'])}</span>**", unsafe_allow_html=True)
            plot_trend(row)

    st.markdown("---")
    st.markdown("## 📈 Weitere Trends mit starkem Wachstum")

    # Platz 4–24 (20 Stück)
    remaining = df.sort_values("Wachstum", ascending=False).dropna().iloc[3:23]
    cols = st.columns(3)

    for i, (_, row) in enumerate(remaining.iterrows()):
        with cols[i % 3]:
            st.markdown(f"### {row['Trend']}")
            st.caption(row["Kategorie"])
            st.markdown(f"**<span style='color:green'>Wachstum: +{row['Wachstum']}%</span>**", unsafe_allow_html=True)
            st.markdown(f"**<span style='color:#3999ff'>Volumen: {int(row['Volumen'])}</span>**", unsafe_allow_html=True)
            plot_trend(row)

