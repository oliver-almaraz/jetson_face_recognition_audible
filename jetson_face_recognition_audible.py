##########################################
# ORIGINAL AGEITGEY'S EXAMPLE SCRIPT:
# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
# 
# SOURCE OF get_jetson_gstreamer_source(): 
# tiny.cc/doorcam2gb
##########################################

import face_recognition
import cv2
import numpy as np

##############################################
# FOR SPEECH DESCRIPTION OF IDENTIFIED FACES #
##############################################

# Import text-to-speech Python library
import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set speech rate (higer = faster)
#engine.setProperty('rate', 100)

# OPTIONAL Set voice
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)


################################################
# AUDIO FEEDBACKTO KNOW SOMETHING IS HAPPENING #
################################################

engine.setProperty('rate', 250)
engine.say("Loading, please wait a minute")
engine.runAndWait()

##################################
# SELECT VIDEO SOURCE (JUST ONE) #
##################################


# Capture video from standard webcam #0 (UNCOMMENT ONLY NEXT LINE)
# video_capture = cv2.VideoCapture(0)


# Capture video from MIPI CSI camera connected to the Jetson Nano (UNCOMMENT NEXT 13 LINES)
# IF YOUR VIDEO IS UPSIDE DOWN, SET THE flip_method TO 2
def get_jetson_gstreamer_source(capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=1, flip_method=2):
    """
    Return an OpenCV-compatible video source description that uses gstreamer to capture video from the RPI camera on a Jetson Nano
    """
    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! ' +
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
            )

video_capture = cv2.VideoCapture(get_jetson_gstreamer_source(), cv2.CAP_GSTREAMER)


############################################
# ADD PATHS TO JPG IMAGES OF "KNOWN FACES" #
# YOU WOULD LIKE TO RECOGNIZE.             #
# BE CAREFUL TO EDIT THE NAME OF THAT FACE #
# EVERY TIME IT APPEARS AS:                #
# NAME_image                               #
# NAME_face_encodings                      #
############################################

elvis_image = face_recognition.load_image_file("elvis.jpeg")
elvis_face_encoding = face_recognition.face_encodings(elvis_image)[0]

churchill_image = face_recognition.load_image_file("churchill.jpeg")
churchill_face_encoding = face_recognition.face_encodings(churchill_image)[0]


######################################
# ADD ALL THE KNOWN FACES' ENCODINGS #
# TO THIS ARRAY, SEPARATED BY COMMA: #
######################################
known_face_encodings = [
	elvis_face_encoding,
	churchill_face_encoding
]

####################################
# ADD THE NAME YOU WANT TO BE READ #
# FOR EVERY KNOWN FACE ENCODING    #
# (FOLLOW THE SAME ORDER)		   #
####################################
known_face_names = [
	"Elvis Presley",
	"Winston Churchill"
]

####################################
# AUDIBLE INSTRUCTIONS FOR EXITING #
####################################

engine.say("Program ready, for exiting please keep pressing for two seconds the keyboard keys control and c")
engine.runAndWait()
engine.setProperty('rate', 100)



while True:

    # Initialize some local variables we must clean in every loop
	face_locations = []
	face_encodings = []
	face_names = []

    # Grab a single frame of video
	ret, frame = video_capture.read()

	# Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_small_frame = small_frame[:, :, ::-1]


	# Find all the faces and face encodings in the current frame of video
	face_locations = face_recognition.face_locations(rgb_small_frame)
	face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

	# A SET SO THAT NO NAME WILL BE REPEATED
	face_names = set()

	for face_encoding in face_encodings:
		# See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		name = "Unknown face"

		# If a match was found in known_face_encodings, just use the known face with the smallest distance to the new face
		face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
		best_match_index = np.argmin(face_distances)
		if matches[best_match_index]:
			name = known_face_names[best_match_index]

		face_names.add(name)

###################################################
# PASS THE RECOGNIZED FACE'S NAME TO PYTTSX3      #
# AND START THE VOICE SYNTH, WAIT UNTIL IT'S DONE #
###################################################
	for name in face_names:
		engine.say(name)
		engine.runAndWait()
		
	face_names.clear()

