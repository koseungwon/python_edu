import cv2
import numpy as np
import datetime
from PIL import ImageFont, ImageDraw, Image

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

font = ImageFont.truetype('fonts/SCDream6.otf', 15)

face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

while True:
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

    ret, frame = capture.read()

    cv2.rectangle(img=frame, pt1=(10,15), pt2=(245, 30), color=(0,0,0), thickness= -1)

    frame = Image.fromarray(frame)
    draw = ImageDraw.Draw(frame)
    draw.text(xy=(10, 15), text="웹캠 테스트" + nowDatetime, font = font, fill=(255,255,255))
    frame = np.array(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5,
                                           minNeighbors=3,
                                           minSize = (20,20))
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor = 1.5,
                                           minNeighbors=3,
                                           minSize = (10,10))

    if len(faces):
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x,y), (x + w, y + h), (255,255, 255), 2, cv2.LINE_4)
    if len(eyes):
        for x, y, w, h in eyes:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2, cv2.LINE_4)

    cv2.imshow("test", frame)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

