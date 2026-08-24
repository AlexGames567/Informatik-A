import streamlit as st
import math

st.set_page_config(
    page_title="Taschenrechner",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Taschenrechner")

# Verlauf initialisieren
if "history" not in st.session_state:
    st.session_state.history = []

# Eingabefelder
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    zahl1 = st.number_input("Erste Zahl", value=0.0, format="%.6f")

with col2:
    operator = st.selectbox(
        "Operator",
        ["+", "-", "×", "÷", "^", "%"]
    )

with col3:
    zahl2 = st.number_input("Zweite Zahl", value=0.0, format="%.6f")

if st.button("Berechnen", type="primary", use_container_width=True):
    try:
        if operator == "+":
            ergebnis = zahl1 + zahl2
        elif operator == "-":
            ergebnis = zahl1 - zahl2
        elif operator == "×":
            ergebnis = zahl1 * zahl2
        elif operator == "÷":
            if zahl2 == 0:
                st.error("Eine Division durch null ist nicht möglich.")
                st.stop()
            ergebnis = zahl1 / zahl2
        elif operator == "^":
            ergebnis = zahl1 ** zahl2
        elif operator == "%":
            ergebnis = zahl1 % zahl2

        rechnung = f"{zahl1:g} {operator} {zahl2:g} = {ergebnis:g}"
        st.session_state.history.append(rechnung)

        st.success(f"Ergebnis: {ergebnis:g}")

    except OverflowError:
        st.error("Das Ergebnis ist zu groß.")
    except Exception as fehler:
        st.error(f"Fehler: {fehler}")

# Verlauf anzeigen
if st.session_state.history:
    st.subheader("Verlauf")

    for rechnung in reversed(st.session_state.history):
        st.write(rechnung)

    if st.button("Verlauf löschen"):
        st.session_state.history = []
        st.rerun()
