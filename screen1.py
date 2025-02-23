import cv2
import mediapipe as mp
import time
from processASL import Finger
from processASL import interpret
import multiprocessing
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image,ImageDraw,ImageFont
import i2cLCD
import time
import pyaudio
import websockets
import asyncio
import base64
import json
import logging

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
auth_key = "49bc7fc00991405fa71af60799da9723"
text = ""
webcamIsOn = True
def talk(stuff):
    sendable = 'espeak "d ' + stuff + '"'
    os.system(sendable)

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
def add_space(text):
    return text + " "

disp = LCD_2inch.LCD_2inch()
disp.Init()
disp.clear()
    
def delete(text):
    return text[:-1]

def clear(text):
    return ""

# Finger objects
THUMB = Finger()
INDEX = Finger()
MIDDLE = Finger()
RING = Finger()
PINKY = Finger()

# captures video from webcam
# NOTE: input value can vary between -1, 0, 1, 2 (differs per device, 0 or 1 is common)
# WARNING: VideoCapture does not work if another application is using camera (ie. video calling)
cap = cv2.VideoCapture(0)

# from pre-trained Mediapipe to draw hand landmarks and connections
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# used to calculate FPS
# pTime = 0  # previous time
# cTime = 0  # current time

while True:
    resultz = False
    # reads image from webcam
    _, img = cap.read()
    h, w, c = img.shape                 # get height, width, depth

    # converts default image value to RGB value
    # NOTE: when printing back to the screen, use default value (img) NOT imgRGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB.flags.writeable = False  # improves performance
    # use Mediapipe to process converted RGB value
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        resultz = True
        for handLms in results.multi_hand_landmarks:
            # creates list of all landmarks for easier indexing
            # list will have 21 values -> lm_list[0] will be first landmark
            lm_list = []

            # id corresponds to landmark #
            #   -> 21 landmarks in total (4 on non-thumb fingers, rest on thumb and palm)
            # lm corresponds to landmark value
            #   -> each lm has x coordinate and y coordinate
            #   -> default values are in ratio (value between 0 and 1)
            #   -> to convert to pixel value, multiple by width and height of screen
            for id, lm in enumerate(handLms.landmark):
                # convert to x, y pixel values
                cx, cy, cz = int(lm.x*w), int(lm.y*h), lm.z*c

                lm_list.append([id, cx, cy, cz])

            # writes text to screen
            cv2.putText(img, str(interpret(lm_list)), (w-300, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (52, 195, 235), 3)

            # draw hand landmarks and connections
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # countdown timer
            curr_time = time.time()
            diff_time = curr_time - prev_time
            if diff_time < 1:
                display_time = 3
            elif diff_time < 2:
                display_time = 2
            elif diff_time <= 3:
                display_time = 1
            cv2.putText(img, str(display_time), (10,70), cv2.FONT_HERSHEY_DUPLEX, 3, (0,0,255), 3)
    else:
        # reset timer when hand not in frame
        prev_time = time.time()
    
    # capture letter of hand every three seconds
    curr_time = time.time()
    if curr_time - prev_time > 3:
        try:
            letters += interpret(lm_list)
        except TypeError:
            pass
        cv2.putText(img, "captured", (w//2 - 200,h//2), cv2.FONT_HERSHEY_DUPLEX, 3, (235, 107, 52), 3)
        prev_time = time.time()
    
    cv2.putText(img, letters, (10, h - 50), cv2.FONT_HERSHEY_DUPLEX, 3, (235, 143, 52), 3)
    
    
    #draw "speak" square
    cv2.rectangle(img, pt1=(640,0), pt2=(540,100), color=(0,0,255), thickness=-1)

    
    # print FPS on screen (not console)
    # cTime = time.time()
    # fps = 1/(cTime-pTime)
    # pTime = cTime
    # cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)

    # print current image captured from webcam
    cv2.imshow("frame", img)                 
    img = cv2.resize(img, (320, 240)) 
    frame = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # if frame is read correctly ret is True
    
    image = frame.rotate(180)
    disp.ShowImage(image)
    
    key = cv2.waitKey(1)
    


    # press Q to quit or "stop" button
    if key == ord("q"):
        break
    if pause == True:
        pausecount = pausecount + 1
        
        if pausecount > 12:
            pause = False
            pausecount = 0
    elif resultz == True:
        if lm_list[8][1] > 540 and lm_list[8][2] < 100:
            print(letters)
            talk(str(letters.lower()))
            letters = ""
            pause = True

# cleanup
cap.release()
cv2.destroyAllWindows()
disp.module_exit()