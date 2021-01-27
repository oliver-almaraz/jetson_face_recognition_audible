# Real-time face recognition with audible (speech) output for Nvidia's Jetson Nano.
Following my last project, the [Food Container Identifier](https://github.com/oliver-almaraz/food_container_identifier), in which I used the Jetson Nano and the software tools provided by [dusty-nv](https://github.com/dusty-nv/jetson-inference) for making a speech descriptor of food containers, I now will use [**ageitgey's** face_recognition](https://github.com/dusty-nv/jetson-inference) Python library for doing almost the same, but with human faces.

If you want to know more about **why it is useful**, please consult my other project's [introduction](https://github.com/oliver-almaraz/food_container_identifier/blob/main/README.md#introduction).

Also both hardware and software **requirements** are the same as my [other project's](https://github.com/oliver-almaraz/food_container_identifier/blob/main/README.md#requirements).

## Installing dependencies
Installing the dependencies is really easy, but it will take a while (more than an hour in the Jetson Nano), since some packages must be compiled from source.
*Note: I assume you already have your Jetson Nano up and running with Jetpack, and that there's a camera conected to it.*

First of all, let's install the system dependencies (if you followed my food_container_identifier project, you already have `python3-pip`, `cmake` and `espeak` installed):

```
$ sudo apt update
$ sudo apt install python3-pip cmake espeak libopenblas-dev liblapack-dev libjpeg-dev
```

Then the Python dependencies (will take a while):
```
$ sudo -H pip3 -v install Cython face_recognition opencv-python pyttsx3
```

## Editing the Python script
I took [**ageigey's example**](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py) and made some changes to fit our hardware and purpose. Basically, like in the food_container_identifier project, I added the speech description features and removed the code related to a visual output.

First, we import and initialize the voice synthetizer's engine:
```python
##############################################
# FOR SPEECH DESCRIPTION OF IDENTIFIED FACES #
##############################################

# Import text-to-speech Python library
import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set speech rate (higer = faster)
# engine.setProperty('rate', 100)

# OPTIONAL Set voice
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)
```

Let's be courteus and add audible instruction for exiting the program, like in foot_container_identifier:
```python
engine.setProperty('rate', 200)
engine.say("Welcome, for exiting this program please keep pressing for two seconds the keyboard keys 'control' and 'c'")
engine.setProperty('rate', 100)
```

Then, we must select a video input source. I'm using the Raspberry Pi V2.1 MIPI CSI cam, so I'm using the second option and commented the first one:
```python
##################################
# SELECT VIDEO SOURCE (JUST ONE) #
##################################


# Capture video from standard webcam #0 (UNCOMMENT ONLY NEXT LINE)
# video_capture = cv2.VideoCapture(0)


# Capture video from MIPI CSI camera connected to the Jetson Nano (UNCOMMENT NEXT 13 LINES)
# IF YOUR VIDEO IS UPSIDE DOWN, SET THE flip_method TO 2
def get_jetson_gstreamer_source(capture_width=1280, capture_height=720, display_width=1280, display_$
    """
    Return an OpenCV-compatible video source description that uses gstreamer to capture video from t$
    """
    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)$
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
            )

video_capture = cv2.VideoCapture(get_jetson_gstreamer_source(), cv2.CAP_GSTREAMER)
```
*Note: I took the get_jetson_gstreamer_source function from another [**ageitgey example**](https://gist.githubusercontent.com/ageitgey/e60d74a0afa3e8c801cff3f98c2a64d3/raw/a49b405ccbf3d4884df2947f30094dad9f4ef8da/doorbell_camera_2gb.py)*

Next, we need to add some **known faces** so that they can be recognized. Save one picture of every face with the name of the person on it on a directory (I suggest it be the same directory as the Python script). There must be only one face per picture. Keep a trace of that directory's path.

In the Python script, let's create objets for our known faces:
```python
############################################
# ADD PATHS TO JPG OR JPEG IMAGES OF       #
# KNOWN FACES YOU WOULD LIKE TO RECOGNIZE. #            #
# BE CAREFUL TO EDIT THE NAME OF THAT FACE #
# EVERY TIME IT APPEARS AS:                #
# NAME_image                               #
# NAME_face_encodings                      #
############################################

elvis_image = face_recognition.load_image_file("elvis.jpeg")
elvis_face_encoding = face_recognition.face_encodings(elvis_image)[0]

churchill_image = face_recognition.load_image_file("churchill.jpeg")
churchill_face_encoding = face_recognition.face_encodings(churchill_image)[0]
```

*Note: if the pictures are in a different directory, you will need to provide an absolute path to them, like `"/home/$USER/Pictures/elvis.jpg"`*

Next, we add those encodings and the names to be displayed to lists:
```python
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
# (FOLLOW THE SAME ORDER)                  #
####################################
known_face_names = [
        "Elvis Presley",
        "Winston Churchill"
]
```

And finally, after making Python recognize the known faces (or an unknown one) when the appear in the video live feed, we pass it's name to the voice engine:
```python
###################################################
# PASS THE RECOGNIZED FACE'S NAME TO PYTTSX3      #
# AND START THE VOICE SYNTH, WAIT UNTIL IT'S DONE #
###################################################
        for (top, right, bottom, left), name in zip(face_locations, face_names):
                engine.say(name)
                engine.runAndWait()
```
## That's it!
We can now test our program running (it will take a minute to load):
```
$ python3 ~/jetson_face_recognition_audible/jetson_face_recognition_audible.py
```
As for the audio output in the Jetson Nano, please refer to my other project's [About audio output](https://github.com/oliver-almaraz/food_container_identifier/blob/main/README.md#about-audio-output) section.
