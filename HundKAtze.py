import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# -----------------------------
# Einstellungen
# -----------------------------

MODEL_PATH = "keras_model.h5"

# Diese Bildgröße muss zur Eingabegröße deines trainierten Modells passen.
# Häufig verwendet werden 150x150, 180x180 oder 224x224.
IMAGE_SIZE = (224, 224)

# Anpassen, falls dein Modell die Klassen andersherum gelernt hat.
# Bei einer Ausgabe wie 0 = Katze und 1 = Hund ist diese Reihenfolge korrekt.
CLASS_NAMES = ["Katze", "Hund"]


# -----------------------------
# Modell laden
# -----------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


try:
    model = load_model()
except Exception as error:
    st.error(f"Das Modell konnte nicht geladen werden: {error}")
    st.stop()


# -----------------------------
# Bild vorbereiten
# -----------------------------

def prepare_image(image):
    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)

    image_array = np.array(image)
    image_array = image_array.astype("float32") / 255.0

    # Batch-Dimension hinzufügen:
    # Aus (224, 224, 3) wird (1, 224, 224, 3)
    image_array = np.expand_dims(image_array, axis=0)

    return image_array


# -----------------------------
# Vorhersage
# -----------------------------

def predict_image(image):
    prepared_image = prepare_image(image)
    prediction = model.predict(prepared_image, verbose=0)

    prediction = np.array(prediction)

    # Fall 1: Binäres Modell mit Sigmoid-Ausgabe, z. B. [[0.82]]
    if prediction.size == 1:
        probability = float(prediction.flatten()[0])

        if probability >= 0.5:
            predicted_class = CLASS_NAMES[1]
            confidence = probability
        else:
            predicted_class = CLASS_NAMES[0]
            confidence = 1 - probability

        probabilities = {
            CLASS_NAMES[0]: 1 - probability,
            CLASS_NAMES[1]: probability
        }

    # Fall 2: Modell mit zwei Ausgabewerten, z. B. [[0.2, 0.8]]
    else:
        probabilities_array = prediction.flatten()
        predicted_index = int(np.argmax(probabilities_array))

        predicted_class = CLASS_NAMES[predicted_index]
        confidence = float(probabilities_array[predicted_index])

        probabilities = {
            CLASS_NAMES[index]: float(probabilities_array[index])
            for index in range(min(len(CLASS_NAMES), len(probabilities_array)))
        }

    return predicted_class, confidence, probabilities


# -----------------------------
# Streamlit-Oberfläche
# -----------------------------

st.set_page_config(
    page_title="Hunde- oder Katzenerkennung",
    page_icon="🐶",
    layout="centered"
)

st.title("🐶🐱 Hunde- oder Katzenerkennung")
st.write("Lade ein Bild hoch, um es mit dem trainierten KI-Modell zu klassifizieren.")

uploaded_file = st.file_uploader(
    "Bild auswählen",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Hochgeladenes Bild",
        use_container_width=True
    )

    with st.spinner("Bild wird analysiert..."):
        predicted_class, confidence, probabilities = predict_image(image)

    st.subheader("Ergebnis")

    if predicted_class == "Hund":
        st.success(
            f"Das Bild zeigt wahrscheinlich einen Hund "
            f"({confidence * 100:.2f} % Sicherheit)."
        )
    else:
        st.info(
            f"Das Bild zeigt wahrscheinlich eine Katze "
            f"({confidence * 100:.2f} % Sicherheit)."
        )

    st.write("Wahrscheinlichkeiten:")

    for class_name, probability in probabilities.items():
        st.write(f"{class_name}: {probability * 100:.2f} %")
        st.progress(float(probability))
