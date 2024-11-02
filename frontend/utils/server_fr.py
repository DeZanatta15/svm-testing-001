import joblib
import numpy as np
import cv2
from flask import Flask, request, jsonify
from deepface import DeepFace

class Modelo:
    def __init__(self):
        # Inicialización de Flask y carga de modelos
        self.app = Flask(__name__)
        self.svm_model = None
        self.label_encoder = None
        self.facenet_model = None

    def cargar_modelos(self):
        # Cargar el modelo SVM y el codificador de etiquetas
        self.svm_model = joblib.load("D:\CodigosH\Proyectos\primeros\pretrained_models\svm_model.pkl")
        self.label_encoder = joblib.load("D:\CodigosH\Proyectos\primeros\pretrained_models\label_encoder.pkl")
        # Cargar el modelo FaceNet de DeepFace
        self.facenet_model = DeepFace.build_model("Facenet")
        print("Modelos cargados exitosamente.")

    def generar_embedding(self, image):
        # Generar el embedding usando el modelo FaceNet
        embedding = DeepFace.represent(img_path=image, model_name="Facenet", detector_backend='mtcnn', enforce_detection=False)[0]['embedding']
        return np.array(embedding)

    def predecir(self):
        try:
            file = request.files['frame'].read()
            nparr = np.frombuffer(file, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            predictions = []
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                embedding = self.generar_embedding(face)

                embedding = embedding.reshape(1, -1)
                prediction = self.svm_model.predict(embedding)
                label = self.label_encoder.inverse_transform(prediction)
                predictions.append(label[0])

            return jsonify({'predictions': predictions})
        except Exception as e:
            return jsonify({'error': str(e)})

    def configurar_rutas(self):
        # Definir las rutas para la API
        self.app.add_url_rule('/predict', 'predict', self.predecir, methods=['POST'])

    def start(self):
        # Llama a todos los procesos en orden
        self.cargar_modelos()
        self.configurar_rutas()
        self.app.run(host='0.0.0.0', port=5001)

# Crear una instancia de la clase y ejecutar la aplicación
if __name__ == '__main__':
    modelo = Modelo()
    modelo.start()
