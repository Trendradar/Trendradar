import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trendradar", layout="wide")

# Seitenmenü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["ℹ️ Trendradar", "📁 Trend Datenbank", "⭐ Favoriten Trends", "📄 Impressum"])

# Daten laden
df = pd.read_csv("trends.csv", encoding="utf-8", sep=",", quotechar='"')
df["Wachstum"] = pd.to_numeric(df["Wachstum"].astype(str).str.replace(",", ""), errors="coerce")
df["Volumen"] = pd.to_numeric(df["Volumen"].astype(str).str.replace(",", ""), errors="coerce")

# Trend-Chart
def plot_trend(row):
    fig, ax = plt.subplots(figsize=(4, 2))
    views = list(map(int, row["Verlauf"].split(",")))
    ax.plot(range(1, len(views) + 1), views, marker="o")
    ax.set_xlabel("Tag")
    ax.set_ylabel("Views")
    st.pyplot(fig)

# Hauptansicht
if page == "ℹ️ Trendradar":
    st.markdown("### 🔥 Top 3 Trends mit höchstem Wachstum")

    df_sorted = df.sort_values("Wachstum", ascending=False).dropna().reset_index(drop=True)
    top3 = df_sorted.iloc[:3]
    remaining = df_sorted.iloc[3:23]  # exakt 20

    cols = st.columns(3)
    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.markdown(f"### {row['Trend']}")
            st.caption(row["Kategorie"])
            st.markdown(f"**<span style='color:green'>Wachstum: +{int(row['Wachstum'])}%</span>**", unsafe_allow_html=True)
            st.markdown(f"**<span style='color:#3999ff'>Volumen: {int(row['Volumen']):,}</span>**", unsafe_allow_html=True)
            plot_trend(row)

    st.markdown("---")
    st.markdown("### 📈 Weitere Trends mit starkem Wachstum")

    # ⭐ Fixiertes Raster mit 3 Spalten pro Zeile (insgesamt 20 Karten sichtbar)
    for i in range(0, len(remaining), 3):
        row_items = remaining.iloc[i:i+3]
        cols = st.columns(3)
        for j, (_, row) in enumerate(row_items.iterrows()):
            with cols[j]:
                st.markdown(f"### {row['Trend']}")
                st.caption(row["Kategorie"])
                st.markdown(f"**<span style='color:green'>Wachstum: +{int(row['Wachstum'])}%</span>**", unsafe_allow_html=True)
                st.markdown(f"**<span style='color:#3999ff'>Volumen: {int(row['Volumen']):,}</span>**", unsafe_allow_html=True)
                plot_trend(row)
