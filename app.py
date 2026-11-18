
import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image

st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="centered"
)

# Load trained model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "plant_disease_model.keras"
    )

model = load_model()

# Load class names
with open("class_names.json", "r") as f:
    class_names = json.load(f)

# Application title
st.title("🌿 Plant Disease Detection System")

st.write(
    "Upload a plant leaf image to identify its disease "
    "using Deep Learning."
)

# Upload image
uploaded_file = st.file_uploader(
    "Upload a leaf image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Plant Leaf",
        use_container_width=True
    )

    if st.button("Predict Disease"):

        # Resize to model's training image size
        img = image.resize((128, 128))

        # Convert to NumPy array
        img_array = np.array(img)

        # Normalize pixel values
        img_array = img_array / 255.0

        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = model.predict(img_array)

        predicted_class = np.argmax(predictions[0])

        confidence = np.max(predictions[0]) * 100

        # Display result
        st.success(
            f"Predicted Disease: {class_names[predicted_class]}"
        )

        st.write(
            f"Confidence: {confidence:.2f}%"
        )

        st.progress(float(confidence / 100))
