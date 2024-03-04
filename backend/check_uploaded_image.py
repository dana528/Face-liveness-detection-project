import cv2
import numpy as np
from flask import Flask, request, jsonify
from keras.models import load_model

app = Flask(__name__)

# Load liveness detection model
model = load_model("livenessdetect/models/anandfinal.hdf5")

# Create face cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route("/process_photo", methods=["POST"])
def process_photo():
    # Get the uploaded photo file
    file = request.files["file"]

    # Convert the uploaded file to bytes
    file_bytes = file.read()

    # Decode the bytes into an image
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform liveness detection on the image
    result = detect_liveness(img)

    # Return the result as JSON
    return jsonify({"final_classification": result})

def detect_liveness(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # If no faces are detected, classify as fake
    if len(faces) == 0:
        return "fake"

    # Extract the face region and preprocess it for liveness detection
    for (x, y, w, h) in faces:
        face_roi = image[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, (128, 128))
        face_normalized = face_resized.astype("float") / 255.0
        face_processed = np.expand_dims(face_normalized, axis=0)

        # Perform liveness detection using the pre-trained model
        (fake, real) = model.predict(face_processed)[0]
        label = "fake" if fake > real else "real"

        return label

if __name__ == "__main__":
    app.run(debug=True)
