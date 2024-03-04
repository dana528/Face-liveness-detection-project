import streamlit as st 
from streamlit_option_menu import option_menu
from PIL import Image
import requests
import json
import subprocess


def home_page():
    st.title("Face Liveness Detection Application")
    st.write("Detect fake faces instantly! Upload a photo or video and let our advanced technology verify its authenticity in real-time. Ensure your security with just a few clicks! Our system will determine whether the uploaded media is genuine or fake.")
    
    st.write("To check a photo, go to the Check Photo page.")
    st.write("To check a video, go to the Check Video page.")

def check_photo_page():
    st.title("Check Photo for Spoofing")
    st.write("Validate the authenticity of facial images instantly. Capture a webcam feed and let our advanced model determine if it's real or fake. Simple, secure, and efficient face liveness detection at your fingertips!")
    
    option = st.radio("Select an option:", ("Capture from Webcam", "Upload a Photo"))
    
    if option == "Capture from Webcam":
        if st.button("Capture"):
            subprocess.run(["python", "backend/mainp.py"])
    elif option == "Upload a Photo":
        uploaded_file = st.file_uploader("Upload a photo:", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Photo", use_column_width=True)
            if st.button("Check Photo"):
                result = process_photo(uploaded_file)
                st.write("Photo processed successfully!")
                st.write("Final prediction:", result)

        
        
def check_video_page():
    st.title("Check Video for Spoofing")
    st.write("Upload a video file and verify its authenticity. Our powerful model analyzes the video content to discern genuine faces from fake ones. Ensure robust security measures against spoofing attempts with our intuitive application.")

    video_file = st.file_uploader("Upload a video:", type=["mp4", "avi"])

    if video_file is not None:
        st.video(video_file)

        # start processing button
        if st.button("Start Detection"): 
            #result = process_video(video_file)
            st.write("Video processed successfully!")
            #st.write("Final prediction:", result)
            


def process_photo(uploaded_file):
    # Prepare the file data for sending
    files = {"file": uploaded_file}  

    # Backend endpoint URL
    url = "http://127.0.0.1:5000/process_photo"

    # Send a POST request to process the photo
    response = requests.post(url, files=files)

    return response



def process_video(video_file):
    # Backend endpoint URL
    url = "http://127.0.0.1:5000/process_video"

    # Prepare the file data for sending
    files = {"file": video_file}

    # Send a POST request to the backend
    response = requests.post(url, files=files)

    if response.status_code == 200:
        try:
            result = response.json()["final_classification"]
            return result
        except json.JSONDecodeError:
            return "Error decoding JSON response from the backend."
    else:
        return "Error processing video. Backend returned status code: {}".format(response.status_code)

with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Check Photo", "Check Video"],
        icons=["house-heart-fill", "camera2", "file-play-fill"],
        menu_icon="emoji-heart-eyes-fill",
        default_index=0,
    )

# Render selected page
if selected == "Home":
    home_page()
        
if selected == "Check Photo":
    check_photo_page()
        
if selected == "Check Video":
    check_video_page()
