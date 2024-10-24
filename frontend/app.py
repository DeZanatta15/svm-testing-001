import streamlit as st
import requests

st.title("Detección de Rostros - API en Render")

# Capturar una imagen con la cámara web
captured_image = st.camera_input("Toma una foto")

if captured_image is not None:
    # URL de la API Flask desplegada en Render
    api_url = "https://svm-api.onrender.com/predict"  # Cambia por tu URL

    # Enviar la imagen a la API
    files = {"frame": captured_image.getvalue()}
    response = requests.post(api_url, files=files)

    if response.status_code == 200:
        predictions = response.json().get("predictions", [])
        st.write(f"Predicciones: {predictions}")
    else:
        st.error(f"Error: {response.json().get('error')}")
