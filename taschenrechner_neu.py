import streamlit as st
import ast
import operator as op
import math

st.set_page_config(
    page_title="Taschenrechner",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Taschenrechner")

# Session-State initialisieren
if "display" not in st.session_state:
    st.session_state.display = ""

if "history" not in st.session_state:
    st.session_state.history = []


# Sichere Berechnung arithmetischer Ausdrücke
def sichere_berechnung(expression):
    expression = expression.replace("×", "*").replace("÷", "/")
    expression = expression.replace("^", "**").replace("%", "/100")

    erlaubte_operatoren = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }

    def berechne(knoten):
        if isinstance(knoten, ast.Constant):
            if isinstance(knoten.value, (int, float)):
                return knoten.value
            raise ValueError("Ungültiger Wert")

        if isinstance(knoten, ast.BinOp):
            operator = erlaubte_operatoren.get(type(knoten.op))
            if operator is None:
                raise ValueError("Ungültiger Operator")

            links = berechne(knoten.left)
            rechts = berechne(knoten.right)

            if isinstance(knoten.op, ast.Div) and rechts == 0:
                raise ZeroDivisionError("Division durch null")

            return operator(links, rechts)

        if isinstance(knoten, ast.UnaryOp):
            operator = erlaubte_operatoren.get(type(knoten.op))
            if operator is None:
                raise ValueError("Ungültiger Operator")
            return operator(berechne(knoten.operand))

        raise ValueError("Ungültiger Ausdruck")

    baum = ast.parse(expression, mode="eval")
    return berechne(baum.body)


# Anzeige
st.text_input(
    "Anzeige",
    value=st.session_state.display,
    disabled=True,
    label_visibility="collapsed"
)

# Tastatur-Layout
tasten = [
    ["AC", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", "^"],
]

# Tasten darstellen
for zeile in tasten:
    spalten = st.columns(4)

    for index, taste in enumerate(zeile):
        with spalten[index]:
            if st.button(
                taste,
                key=f"taste_{taste}_{tasten.index(zeile)}",
                use_container_width=True
            ):
                if taste == "AC":
                    st.session_state.display = ""

                elif taste == "⌫":
                    st.session_state.display = st.session_state.display[:-1]

                elif taste == "=":
                    if st.session_state.display:
                        try:
                            ausdruck = st.session_state.display
                            ergebnis = sichere_berechnung(ausdruck)

                            if isinstance(ergebnis, float) and ergebnis.is_integer():
                                ergebnis = int(ergebnis)

                            st.session_state.history.append(
                                f"{ausdruck} = {ergebnis}"
                            )
                            st.session_state.display = str(ergebnis)

                        except ZeroDivisionError:
                            st.error("Division durch null ist nicht möglich.")
                        except Exception:
                            st.error("Ungültiger Ausdruck.")

                else:
                    # Verhindert mehrere Dezimalpunkte in derselben Zahl
                    if taste == ".":
                        letzte_zahl = st.session_state.display.split("+")[-1]
                        letzte_zahl = letzte_zahl.split("-")[-1]
                        letzte_zahl = letzte_zahl.split("×")[-1]
                        letzte_zahl = letzte_zahl.split("÷")[-1]

                        if "." in letzte_zahl:
                            st.stop()

                    st.session_state.display += taste

                st.rerun()


# Verlauf
if st.session_state.history:
    st.subheader("Verlauf")

    for eintrag in reversed(st.session_state.history):
        st.write(eintrag)

    if st.button("Verlauf löschen", use_container_width=True):
        st.session_state.history = []
        st.rerun()
