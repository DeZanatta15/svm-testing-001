import streamlit as st
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import json
import requests

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.camera_icon = "📸"
        self.frame = None
        self.api_base_url = "http://localhost:8000" #"Replace with the correct API"
        #self.flask_server = "http://localhost:5001/predict" #"Replace with the correct Flask server"

    def transform(self, frame):
        self.frame = frame.to_ndarray(format="bgr24")

        # Optionally, resize frame to reduce processing time
        resized_frame = cv2.resize(self.frame, (320, 240))

        # Display message on the frame (Optional)
        cv2.putText(resized_frame, "Press q to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Return the processed frame
        return av.VideoFrame.from_ndarray(resized_frame, format="bgr24")

    def db_conection(self):
        # Mock Database (For demonstration purposes, replace this with real DB connections later)
        #mock_db = {"user@example.com": {"password": "password123", "name": "John Doe"}}
        pass

    def set_UI(self, txt_introductivo: str):
        # Streamlit UI setup
        st.title("Face Recognition: Pass List")
        st.write(txt_introductivo)

        # Botón para tomar la foto con el icono de la cámara
        if st.button(f"Take Picture {self.camera_icon}"):
            self.take_picture()

        # Vista previa usando streamlit-webrtc
        webrtc_ctx = webrtc_streamer(
            key="camera",
            video_transformer_factory=VideoTransformer,
            media_stream_constraints={"video": True, "audio": False},
        )

        if webrtc_ctx.video_transformer:
            self.capture_photo(webrtc_ctx)

        st.write("Press the button to activate the Camera")

    def take_picture(self):
        """Placeholder method for taking a picture"""
        st.write("Picture taken!")

    def capture_photo(self, webrtc_ctx):
        """Capture the frame from the WebRTC stream and save it"""
        try:
            if webrtc_ctx.video_transformer and webrtc_ctx.video_transformer.frame is not None:
                captured_frame = webrtc_ctx.video_transformer.frame
                # Save the captured frame
                cv2.imwrite("captured_photo.png", captured_frame)
                st.image("captured_photo.png", caption="Captured Photo")
        except Exception as e:
            st.error(f"Error capturing photo: {e}")

    def selection(self):
        menu = ["Login", "Sign Up"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            self.login()

        elif choice == "Sign Up":
            self.sign_up()

    def login(self):
        """ Streamlit UI setup of the log in"""

        st.subheader("Login to your Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Prepare login data
            try:
                if email == "user@example.com" and password == "password123":
                    st.success("Logged in successfully")
                    user_data = {"full_name": "John Doe", "role": "teacher"}  # Mock response data
                    self.teacher_dashboard(user_data)
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Error during login: {e}")

    def sign_up(self):
        st.subheader("Create New Account")

        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Student", "Teacher"])

        if st.button("Sign Up"):
            # Prepare registration data
            sign_up_data = {
                "full_name": full_name,
                "email": email,
                "password": password,
                "role": role
            }
            # Send POST request to API to register user
            try:
                response = requests.post(f"{self.api_base_url}/register", json=sign_up_data)
                if response.status_code == 201:
                    st.success("Account created successfully")
                else:
                    st.error("Error creating account")
            except Exception as e:
                st.error(f"Error during sign up: {e}")

    def teacher_dashboard(self, user_data):
        st.subheader(f"Welcome {user_data['full_name']} (Teacher)")
        st.write("You have access to your classes.")
        # Placeholder for future class management implementation

    def student_dashboard(self, user_data):
        st.subheader(f"Welcome {user_data['full_name']} (Student)")
        st.write("You can mark your attendance.")
        # Placeholder for future attendance functionality

    def start(self, txt_introductivo: str):
        self.set_UI(txt_introductivo)
        
# Texto introductorio para el pase de lista
txt_introductivo = """
Usually when the teacher arrives to the classroom, the students are already there and ready for the class, 
so the teacher should take attendance of the students. For attendance, they have to open a link and pass the 
face recognition. The time of the recognition is saved, and then the teacher evaluates if the student was on time or not.
"""

# Función principal para evitar la ejecución accidental del código
def main():
    try:
        camara = VideoTransformer()
        camara.start(txt_introductivo)
    except Exception as e:
        st.error(f"Error starting the application: {e}")

if __name__ == "__main__":
    video_transformer = VideoTransformer()
    video_transformer.start(txt_introductivo)