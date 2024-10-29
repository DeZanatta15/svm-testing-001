import cv2
import requests

class Web_cam:
    def __init__(self):
        """Initialize the WebcamClient with the Flask server URL and camera."""
        #self.url = url
        self.cap = cv2.VideoCapture(0)  # Open the default webcam

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def capture_frame(self):
        """Capture a frame from the webcam and resize it."""
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            return None

        # Resize frame to reduce processing time
        frame = cv2.resize(frame, (320, 240))
        return frame

    def send_frame_to_server(self, frame):
        """Send the captured frame to the Flask server for prediction."""
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(self.url, files={'frame': img_encoded.tobytes()})
        return response

    def display_frame(self, frame):
        """Display the webcam feed."""
        cv2.imshow('Webcam', frame)

    def release_resources(self):
        """Release the webcam and close windows."""
        self.cap.release()
        cv2.destroyAllWindows()

    def run(self):
        """Run the main loop to capture, send, and display webcam frames."""
        while True:
            frame = self.capture_frame()
            if frame is None:
                break

            # Send the frame to the server
            response = self.send_frame_to_server(frame)

            # Print the server's response
            print("Server response:", response.json())

            # Display the frame
            self.display_frame(frame)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.release_resources()

    def start(self):
        """Start the WebcamClient."""
        self.run()

# Main function to run the WebcamClient
def main():
    flask_url = "http://localhost:5001/predict"  # Set the URL of your Flask server
    webcam_client = (flask_url)
    webcam_client.run()

if __name__ == "__main__":
    web_cam = Web_cam()
    web_cam.start()
