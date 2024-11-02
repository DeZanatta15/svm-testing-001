import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av
import json
import requests

class Camera:

    def __init__(self):
        self.camera_icon = "📸"
        self.frame = None
        self.api_base_url = "http://localhost:8000" #"Replace with the correct API"
        #self.flask_server = "http://localhost:5001/predict" #"Replace with the correct Flask server"

    def db_conection(self):
        # Mock Database (For demonstration purposes, replace this with real DB connections later)
        #mock_db = {"user@example.com": {"password": "password123", "name": "John Doe"}}
        pass

    def set_UI(self, txt_introductivo: str):
        # Streamlit UI setup
        st.title("Face Recognition: Pass List")
        st.subheader("Welcome to the Face Recognition App")
        st.divider()
        st.text(txt_introductivo)

    def home_page(self):
        st.title("Face Recognition: Pass List")
        st.subheader("Welcome to the Face Recognition App")
        st.write("This app uses face recognition to take attendance of students in a classroom.")
        st.write("Please select an option from the sidebar to get started.")

    def activate_camera(self):
        # Preview using streamlit-webrtc
        webrtc_ctx = webrtc_streamer(
            key="camera",
            media_stream_constraints={"video": True, "audio": False})

        if webrtc_ctx.state.playing:
            st.info("Camera is active")
            if st.button("Take Picture"):
                self.capture_photo(webrtc_ctx)
            if st.toggle("Accept and Upload Photo"):
                self.upload_photo()
        else:
            st.warning("Camera is not active")

    def camera_try(self):
        enable = st.toggle("Enable camera")
        picture = st.camera_input("Take a picture", disabled=not enable)

        if picture:
            st.image(picture)
            with st.form(key="photo_form"):
                save = st.form_submit_button("Save")
                cancel = st.form_submit_button("Cancel")

                if save:
                    self.save_photo(picture)
                elif cancel:
                    st.warning("Photo not saved. You can take another picture.")

    def save_photo(self, picture):
        """Save the captured photo to the database"""
        try:
            # Convert the picture to a format suitable for saving
            img = cv2.imdecode(np.frombuffer(picture.read(), np.uint8), cv2.IMREAD_COLOR)
            cv2.imwrite("saved_photo.png", img)
            st.success("Photo saved successfully")
            # Here you can add code to save the photo to a database
        except Exception as e:
            st.error(f"Error saving photo: {e}")

    def capture_photo(self, webrtc_ctx):
        """Capture the frame from the WebRTC stream and save it"""
        try:
            if webrtc_ctx.video_receiver:
                frame = webrtc_ctx.video_receiver.get_frame()
                captured_frame = frame.to_ndarray(format="bgr24")
                # Save the captured frame
                cv2.imwrite("captured_photo.png", captured_frame)
                st.image("captured_photo.png", caption="Captured Photo")
        except Exception as e:
            st.error(f"Error capturing photo: {e}")

    def navigate_tabs(self):
        tabs = st.tabs(["Home page", "Camera", "Login/Sign Up"])
        with tabs[0]:
            self.home_page()
        with tabs[1]:
            self.camera_try()
        with tabs[2]:
            self.selection()

    def selection(self):
        menu = ["Login", "Sign Up"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            self.login()

        elif choice == "Sign Up":
            self.sign_up()

#Asistencia, dasboard y registrar nueva persona 

    def start(self, txt_introductivo: str):
        self.set_UI(txt_introductivo)
        self.camera_try()


# Texto introductorio para el pase de lista
txt_introductivo = """
Usually when the teacher arrives to the classroom, the students are already there and ready for the class, 
so the teacher should take attendance of the students. For attendance, they have to open a link and pass the 
face recognition. The time of the recognition is saved, and then the teacher evaluates if the student was on time or not.
"""

# Función principal para evitar la ejecución accidental del código
def main():
    try:
        camara = Camera()
        camara.start(txt_introductivo)
    except Exception as e:
        st.error(f"Error starting the application: {e}")

if __name__ == "__main__":
    main()
