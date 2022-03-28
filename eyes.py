import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture(1)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640,360,[20,50])
eyesOpen = True
color = (255,0,255)
eyeImage = cv2.imread("eyes_animation/open.tiff")
counter = 0
seedImage = cv2.imread("seed_animation/seed-1.png")

idList = [22,23,24,26,110,157,158,159,160,161,130,243]

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5, (255, 0, 255), cv2.FILLED)

        
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
            eyesOpen = True
            eyeImage = cv2.imread("eyes_animation/open.tiff")
            counter = 1
        else: 
            eyesOpen = False
            eyeImage = cv2.imread("eyes_animation/closed.tiff")
            if counter < 30:
                counter += 1
    
        seedImage = cv2.imread(f'seed_animation/seed-{counter}.png')
        cvzone.putTextRect(img, f'Eyes Open: {eyesOpen}', (50,100), colorR=color)
        #print(eyesOpen)

        cv2.imshow('eyesAnimation', eyeImage)
        cv2.imshow('seedAnimation', seedImage)

        #imgPlot = plotY.update(ratio)
        #cv2.imshow('imagePlot', imgPlot)
    
    img = cv2.resize(img, (640, 360))
    cv2.imshow('image', img)
    cv2.waitKey(25)