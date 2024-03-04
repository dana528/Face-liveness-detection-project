# this code is for detect real/fake faces in a given video.first i implemented this and then changed it.

# from keras.models import load_model
# import cv2
# import numpy as np 

# # Load liveness detection model (assuming you have a model loaded as 'model')
# model = load_model("livenessdetect/models/anandfinal.hdf5")

# # Create a videocapture object & read from input file
# cap = cv2.VideoCapture('videos/Deewana _ Dance _ ABCD Dance Factory _ Choreo _ #Shorts.mp4')

# # Create face cascade classifier
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# # Read until video is completed
# while True:
#     # Capture frame by frame
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # Convert the video into gray video without color
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     # Detect faces in the video
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
#     # For each detected face
#     for (x, y, w, h) in faces:
#         # Extract face region
#         face_roi = frame[y:y+h, x:x+w]

#         # Preprocess face region for liveness detection
#         face_resized = cv2.resize(face_roi, (128, 128))
#         face_normalized = face_resized.astype("float") / 255.0
#         face_processed = np.expand_dims(face_normalized, axis=0)
        
#         # Perform liveness detection
#         (fake, real) = model.predict(face_processed)[0]
        
#         # Label the face based on prediction
#         label = "fake" if fake > real else "real"
        
#         # Draw rectangle boxes around the faces
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        
#         # Put text label on the frame
#         cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
#     # Display the resulting frame
#     cv2.imshow('Frame', frame)
    
#     # Press 'q' on keyboard to exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything is done, release the videocapture object
# cap.release()

# # Closes all the frames
# cv2.destroyAllWindows()


# here is the corrected code it will classify a video as a fake or a real 

from flask import Flask, request, send_file
from keras.models import load_model
import cv2
import numpy as np
import os
import tempfile

app = Flask(__name__)

# First load liveness detection model 
model = load_model("livenessdetect/models/anandfinal.hdf5")

# Create face cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route("/process_video", methods=["POST"])
def process_video():
    video_file = request.files["file"]  

    # Save the video file to a temporary location
    video_path = os.path.join(tempfile.gettempdir(), "uploaded_video.mp4")
    video_file.save(video_path)

    # Process the uploaded video
    process_video_frames(video_path)

    # Return a response
    return "Video processing completed"



def process_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    predictions = []  # List to store predictions from each frame
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (128, 128))
            face_normalized = face_resized.astype("float") / 255.0
            face_processed = np.expand_dims(face_normalized, axis=0)
            (fake, real) = model.predict(face_processed)[0]
            label = "fake" if fake > real else "real"
            predictions.append(label)
            
            # then draw rectangle and label on the frame
            color = (0, 255, 0) if label == "real" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # then display the processed frame
        cv2.imshow('Processed Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # Determine final classification based on majority vote
    if "real" in predictions and "fake" in predictions:
        final_prediction = "real" if predictions.count("real") > predictions.count("fake") else "fake"
    elif "real" in predictions:
        final_prediction = "final prediction = real"
    else:
        final_prediction = "final prediction = fake"

    print("Final classification:", final_prediction)



if __name__ == "__main__":
    app.run(debug=True)

