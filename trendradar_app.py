import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Trendradar", layout="wide")

# Style: saubere Typografie & weiches Design
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4 {
            font-weight: 600;
            margin-bottom: 0.3em;
        }
        .trend-card {
            background-color: #f9f9f9;
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        }
        .top-trend-card {
            background-color: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        }
    </style>
""", unsafe_allow_html=True)

# Menü
st.sidebar.title("🧠 Trendradar")
page = st.sidebar.radio("Navigation", ["ℹ️ Trendradar", "📂 Trend Datenbank", "⭐ Favoriten Trends", "🧾 Impressum"])

# Daten laden
df = pd.read_csv("trends.csv", encoding="utf-8")
df["Wachstum"] = pd.to_numeric(df["Wachstum"], errors="coerce")
df["Volumen"] = pd.to_numeric(df["Volumen"].astype(str).str.replace(",", ""), errors="coerce")

# Chart Funktion
def plot_trend(row):
    fig, ax = plt.subplots(figsize=(4, 2))
    views = list(map(int, row["Verlauf"].split(",")))
    ax.plot(range(1, len(views) + 1), views, marker="o")
    ax.set_xlabel("Tag")
    ax.set_ylabel("Views")
    ax.tick_params(axis='both', labelsize=8)
    st.pyplot(fig)

# Hauptseite
if page == "ℹ️ Trendradar":
    st.markdown("<h2 style='margin-bottom: 0.5em;'>🔥 Top 3 Trends mit höchstem Wachstum</h2>", unsafe_allow_html=True)
    top3 = df.sort_values("Wachstum", ascending=False).head(3)
    cols = st.columns(3)
    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.markdown(f"<div class='top-trend-card'>", unsafe_allow_html=True)
            st.markdown(f"<h4>{row['Trend']}</h4>", unsafe_allow_html=True)
            st.caption(row["Kategorie"])
            st.markdown(f"<span style='color:green; font-weight:bold;'>Wachstum: +{int(row['Wachstum'])}%</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#007bff;'>Volumen: {int(row['Volumen']):,}</span>", unsafe_allow_html=True)
            plot_trend(row)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:2em;'>📈 Weitere Trends mit starkem Wachstum</h3>", unsafe_allow_html=True)
    remaining = df.sort_values("Wachstum", ascending=False).dropna().iloc[3:23]

    for i in range(0, len(remaining), 3):
        row_slice = remaining.iloc[i:i+3]
        cols = st.columns(3)
        for col, (_, row) in zip(cols, row_slice.iterrows()):
            with col:
                st.markdown(f"<div class='trend-card'>", unsafe_allow_html=True)
                st.markdown(f"<h5>{row['Trend']}</h5>", unsafe_allow_html=True)
                st.caption(row["Kategorie"])
                st.markdown(f"<span style='color:green; font-weight:bold;'>Wachstum: +{int(row['Wachstum'])}%</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='color:#007bff;'>Volumen: {int(row['Volumen']):,}</span>", unsafe_allow_html=True)
                plot_trend(row)
                st.markdown("</div>", unsafe_allow_html=True)
