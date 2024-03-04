Face Liveness Detection Project
Overview
This project implements face liveness detection using Convolutional Neural Networks (CNNs) and Computer Vision techniques. It distinguishes between real and fake faces in real-time environments and pre-recorded videos. The CNN model is trained on depth maps of images to achieve accurate detection.

File Structure
mainp.py: This script is used for photo face liveness detection.
main.py: This script is used for video face liveness detection.
livenessdetect/
training.py: Contains parameter tuning steps for the model.
model.py: Defines the CNN architecture for training the dataset.
utils.py: Implements the predictperson function for mainp.py.
models/
anandfinal.hdf5: Pre-trained model for liveness detection.
haarcascade_frontalface_default.xml: Haar cascade classifier for face detection.
CNN Architecture
The CNN model consists of 3 hidden convolutional layers with ReLU activation functions and 1 fully connected layer. It is trained with 10 epochs and a batch size of 32. The training-to-testing ratio is 75:25.

Usage
Real-time Face Liveness Detection (Photo)
To detect face liveness in real-time using webcam input:

Clone the repository:

bash
Copy code
git clone https://github.com/anand498/Face-Liveness-Detection.git
Install the required dependencies:

Copy code
pip install -r requirements.txt
Run the photo face liveness detection script:

Copy code
python mainp.py
Face Liveness Detection in Videos
To detect face liveness in pre-recorded videos:

Clone the repository and install dependencies as mentioned above.

Run the video face liveness detection script:

css
Copy code
python main.py
Upload the video file you want to analyze for face liveness.

Start the detection process.

Wait for the analysis to complete, and the results will be displayed indicating whether the faces in the video are real or fake.

Note
Ensure that the video file you upload is in a compatible format (e.g., .mp4, .avi) and contains clear facial images for accurate detection results.