import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trendradar", layout="wide")

# Menü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["ℹ️ Trendradar", "📁 Trend Datenbank", "⭐ Favoriten Trends", "📄 Impressum"])

# CSV laden
df = pd.read_csv("trends.csv", encoding="utf-8", sep=",", quotechar='"')

# Spalten umwandeln
df["Wachstum"] = pd.to_numeric(df["Wachstum"].astype(str).str.replace(",", ""), errors="coerce")
df["Volumen"] = pd.to_numeric(df["Volumen"].astype(str).str.replace(",", ""), errors="coerce")

# Debug: Zeige alle geladenen Trends
st.subheader("🧪 Debug: Zeige alle verfügbaren Trends")
st.write(df[["Trend", "Wachstum", "Volumen"]])
st.write(f"📦 Gesamte Zeilen im geladenen DataFrame: {df.shape[0]}")

# Trends sortieren & bereinigen
df_sorted = df.sort_values("Wachstum", ascending=False).dropna().reset_index(drop=True)
st.write("✅ Nach Sortierung & dropna:", df_sorted.shape)

# Chart Funktion
def plot_trend(row):
    fig, ax = plt.subplots(figsize=(4, 2))
    views = list(map(int, row["Verlauf"].split(",")))
    ax.plot(range(1, len(views) + 1), views, marker="o")
    ax.set_xlabel("Tag")
    ax.set_ylabel("Views")
    st.pyplot(fig)

# Hauptseite
if page == "ℹ️ Trendradar":
    st.markdown("## 🔥 Top 3 Trends mit höchstem Wachstum")

    top3 = df_sorted.iloc[:3]
    for i, (_, row) in enumerate(top3.iterrows()):
        st.markdown(f"### [{i+1}] {row['Trend']}")
        st.caption(row["Kategorie"])
        st.markdown(f"**<span style='color:green'>Wachstum: +{int(row['Wachstum'])}%</span>**", unsafe_allow_html=True)
        st.markdown(f"**<span style='color:#3999ff'>Volumen: {int(row['Volumen']):,}</span>**", unsafe_allow_html=True)
        plot_trend(row)

    st.markdown("---")
    st.markdown("## 📈 Weitere Trends mit starkem Wachstum")

    remaining = df_sorted.iloc[3:23]
    st.write(f"📊 Anzahl Trends Platz 4–24: {len(remaining)}")

    for idx, (_, row) in enumerate(remaining.iterrows(), start=4):
        st.markdown(f"### [{idx}] {row['Trend']}")
        st.caption(row["Kategorie"])
        st.markdown(f"**<span style='color:green'>Wachstum: +{int(row['Wachstum'])}%</span>**", unsafe_allow_html=True)
        st.markdown(f"**<span style='color:#3999ff'>Volumen: {int(row['Volumen']):,}</span>**", unsafe_allow_html=True)
        plot_trend(row)

