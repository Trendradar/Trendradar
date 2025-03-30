import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trendradar", layout="wide")

# Seitenmenü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["ℹ️ Trendradar", "📂 Trend Datenbank", "⭐ Favoriten Trends", "ℹ️ Impressum"])

# Daten laden
df = pd.read_csv("trends.csv")

# Trend-Chart zeichnen
def plot_trend(row):
    fig, ax = plt.subplots(figsize=(4, 2))
    views = list(map(int, row["Verlauf"].split(",")))
    ax.plot(range(1, len(views) + 1), views, marker="o")
    ax.set_title("")
    ax.set_xlabel("Tag")
    ax.set_ylabel("Views")
    st.pyplot(fig)

# Hauptseite: Trendradar
if page == "ℹ️ Trendradar":
    st.markdown("## 🔥 Top 3 Trends mit höchstem Wachstum")
    top3 = df.sort_values("Wachstum", ascending=False).head(3)
    cols = st.columns(3)

    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.markdown(f"### {row.Trend}")
            st.caption(row.Kategorie)
            st.markdown(f"**<span style='color:green'>Wachstum: +{row.Wachstum}%</span>**", unsafe_allow_html=True)
            st.markdown(f"**<span style='color:#3999ff'>Volumen: {row.Volumen:,}</span>**", unsafe_allow_html=True)
            plot_trend(row)

    st.markdown("---")
    st.markdown("## 📈 Weitere Trends mit starkem Wachstum")
    remaining = df.sort_values("Wachstum", ascending=False).iloc[3:23]

    cols = st.columns(3)

    for i, (_, row) in enumerate(remaining.iterrows()):
        with cols[i % 3]:
            st.markdown(f"### {row.Trend}")
            st.caption(row.Kategorie)
            st.markdown(f"**<span style='color:green'>Wachstum: +{row.Wachstum}%</span>**", unsafe_allow_html=True)
            st.markdown(f"**<span style='color:#3999ff'>Volumen: {row.Volumen:,}</span>**", unsafe_allow_html=True)
            plot_trend(row)
