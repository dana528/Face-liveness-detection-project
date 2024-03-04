from xml.etree.ElementTree import tostring
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os,cv2
import ctypes


model = load_model("livenessdetect/models/anandfinal.hdf5")
faceCascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def predictperson():
	WINDOW_NAME = 'Full Integration'
	video_capture = cv2.VideoCapture(0)
	# Full screen mode
	cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	while(True):
		 # get Screen Size
		user32 = ctypes.windll.user32
		screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
	
	# read video frame by frame
		ret, frame = video_capture.read()

		frame = cv2.flip(frame, 1)

		frame_height, frame_width, _ = frame.shape

		scaleWidth = float(screen_width)/float(frame_width)
		scaleHeight = float(screen_height)/float(frame_height)

		if scaleHeight>scaleWidth:
				imgScale = scaleWidth

		else:
				imgScale = scaleHeight

		newX,newY = frame.shape[1]*imgScale, frame.shape[0]*imgScale
		frame = cv2.resize(frame,(int(newX),int(newY)))
		# cv2.imshow(WINDOW_NAME, frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
					break 
		# ret,frame = video_capture.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),)
		cv2.rectangle(frame, (100, 100), (900, 950), (255,0,0), 2)
		
		cv2.putText(frame,"Please keep your head inside the blue box and have only one face in the frame", (10, 700),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		faces_inside_box = 0
		for (x, y, w, h) in faces:
			# if x<800 and x>400 and y<300 and y>100 and (x+w)<900 and (x+w)>400 and (y+h)<560 and (y+h)>100:
				faces_inside_box+=1
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

		if faces_inside_box > 1 :
			cv2.putText(frame,"Multiple Faces detected!", (600, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		if faces_inside_box == 1 :
			print ("X:", x)
			print("Y:", y)
			if x<900 and x>100 and y<600 and y>100 and (x+w)<900 and (x+w)>400 and (y+h)<560 and (y+h)>100:
				image = cv2.resize(frame, (128, 128))
				image = image.astype("float") / 255.0
				image = img_to_array(image)
				image = np.expand_dims(image, axis=0)
				( fake, real) = model.predict(image)[0]
				if fake > real:
					label = "fake"
				else:
					label= "real"
				
				cv2.putText(frame,label, (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			else:
				cv2.putText(frame,"Please come closer to the camera", (10, 390),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.imshow("Frame",frame)

