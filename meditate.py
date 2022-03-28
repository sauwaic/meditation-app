import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import streamlit as st 
from PIL import Image
import time
from streamlit_player import st_player

st.title('Growth happens when you close your eyes')
st.subheader('Plant a seed and let it blossom in 1 minute')

run = st.checkbox('Start')
EYES_WINDOW = st.image([], width=50)
SEED_WINDOW = st.image([])
cap = cv2.VideoCapture(1)
detector = FaceMeshDetector(maxFaces=1)
image = Image.open("eyes_animation/open.tiff")
eyesOpen = True
#st.image(image)
lengthHor = 0
lengthVer = 0
counter = 1

st.write("Optional guided meditation")
st_player('https://youtu.be/LDs7jglje_U?t=75')

while True:
    success, img = cap.read() 

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVer,_ = detector.findDistance(leftUp, leftDown)
        lengthHor,_ = detector.findDistance(leftLeft, leftRight)
        cv2.line(img,leftUp,leftDown, (0,200,0), 3)
        cv2.line(img,leftLeft,leftRight, (0,200,0), 3)
        #print(lengthHor)
        
        ratio = (lengthVer/lengthHor) * 100
        if ratio > 35:
            eyeOpen = True
            imgEye = Image.open("eyes_animation/open_cropped.tiff")
            #eyeImage = cv2.imread("eyes_animation/open.tiff")
            #counter = 1
        else: 
            eyesOpen = False
            #eyeImage = cv2.imread("eyes_animation/closed.tiff")
            imgEye = Image.open("eyes_animation/closed_cropped.tiff")
            if run:
                if counter < 30:
                    time.sleep(10)
                    counter += 1

    EYES_WINDOW.image(imgEye)
    if run:
        SEED_WINDOW.image(f'seed_animation/jpg/seed-{counter}.jpg')

