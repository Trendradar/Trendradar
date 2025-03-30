import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trendradar", layout="wide")

# Seitenmenü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["ℹ️ Trendradar", "📁 Trend Datenbank", "⭐ Favoriten Trends", "📄 Impressum"])

# CSV laden
df = pd.read_csv("trends.csv", encoding="utf-8", sep=",", quotechar='"')
df["Wachstum"] = pd.to_numeric(df["Wachstum"].astype(str).str.replace(",", ""), errors="coerce")
df["Volumen"] = pd.to_numeric(df["Volumen"].astype(str).str.replace(",", ""), errors="coerce")

# Debug-Ausgabe des DataFrames
st.write("📊 Gesamte Datenmenge (nach Laden und Umwandlung):", df.shape)
st.write(df.head(5))

# Funktion: Verlauf als Liniendiagramm anzeigen
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

    df_sorted = df.sort_values("Wachstum", ascending=False).dropna().reset_index(drop=True)
    st.write("✅ Sortierte & bereinigte Daten:", df_sorted.shape)

    top3 = df_sorted.iloc[:3]
    for i, (_, row) in enumerate(top3.iterrows()):
        st.markdown(f"### [{i+1}] {row['Trend']}")
        st.write(f"Kategorie: {row['Kategorie']}")
        st.write(f"Wachstum: {row['Wachstum']}%")
        st.write(f"Volumen: {row['Volumen']}")
        plot_trend(row)

    st.markdown("---")
    st.markdown("## 📈 Weitere Trends mit starkem Wachstum")

    remaining = df_sorted.iloc[3:23]  # Platz 4–24
    st.write(f"Anzahl weiterer Trends: {len(remaining)} (Sollte 20 sein)")

    for idx, (_, row) in enumerate(remaining.iterrows(), start=4):
        st.markdown(f"### [{idx}] {row['Trend']}")
        st.write(f"Kategorie: {row['Kategorie']}")
        st.write(f"Wachstum: {row['Wachstum']}%")
        st.write(f"Volumen: {row['Volumen']}")
        plot_trend(row)

