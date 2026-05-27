"""
EcoMonitor – dashboard.py
Dashboard Streamlit con tabella, statistiche e grafici.
Avvio: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import os

CSV_FILE = "misure.csv"

st.set_page_config(page_title="EcoMonitor Dashboard", layout="wide")

st.title(" EcoMonitor – Dashboard ambientale")
st.caption("Dati raccolti dagli studenti tramite phyphox")

# ── Carica dati ────────────────────────────────────────────────────────────────
if not os.path.exists(CSV_FILE):
    st.warning(f"File '{CSV_FILE}' non trovato. Avvia il server e invia almeno una misura.")
    st.stop()

df = pd.read_csv(CSV_FILE)

if df.empty:
    st.info("Nessun dato disponibile. Invia qualche misura dal client.")
    st.stop()

# Conversione della colonna data_ora
df["data_ora"] = pd.to_datetime(df["data_ora"], errors="coerce")
df["valore"] = pd.to_numeric(df["valore"], errors="coerce")

# ── Metriche riepilogative ──────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Misure totali", len(df))
col2.metric("Valore medio", f"{df['valore'].mean():.1f}")
col3.metric("Studenti", df["studente"].nunique())

st.divider()

# ── Tabella completa ────────────────────────────────────────────────────────────
st.subheader(" Tutte le misure")
st.dataframe(df, use_container_width=True)

st.divider()

# ── Grafico: misure per luogo ───────────────────────────────────────────────────
st.subheader(" Valore medio per luogo")
media_luogo = df.groupby("luogo")["valore"].mean().reset_index()
media_luogo.columns = ["Luogo", "Valore medio"]
st.bar_chart(media_luogo.set_index("Luogo"))

# ── Grafico: misure per studente ────────────────────────────────────────────────
st.subheader(" Numero di misure per studente")
conteggio = df["studente"].value_counts().reset_index()
conteggio.columns = ["Studente", "Numero misure"]
st.bar_chart(conteggio.set_index("Studente"))
