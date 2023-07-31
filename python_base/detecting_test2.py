import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

face_id = input('\n enter user id and press <return> ==>')
print("\n [INFO] Initializing face capture. Look the Camera and wait")

count=0

while True:
    ret, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 6)

    if len(faces):
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),2)
            count+=1
            cv2.imwrite('data/'+str(face_id)+'.'+str(count)+".jpg",
                        gray[y:y+h, x:x+w])
    cv2.imshow('image', frame)

    if cv2.waitKey(1)>0: break
    elif count>=100: break
print(count)
capture.release()
cv2.destroyAllWindows()

from PIL import Image
import os

detector = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

path = 'data/'
recognizer = cv2.face.LBPHFaceRecognizer_create()

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

    faceSamples=[]
    ids=[]
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[0])
        faces = detector.detectMultiScale(img_numpy)
        for(x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
    return faceSamples, ids
print('\n [INFO] Training Faces wait...')
faces, ids = getImagesAndLabels(path)

recognizer.train(faces, np.array(ids))
recognizer.write('face-trainner.yml')
print('\n [INFO] {0}  faces trained. Exiting Program'.format(len(np.unique(ids))))

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face-trainner.yml')
cascadePath = 'haarcascade/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_COMPLEX
id = 0

names = ['None', 'shpark', 'obama', 'Trump', 'sunoo']

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

minW = 0.1 * cam.get(cv2.CAP_PROP_FRAME_WIDTH)
minH = 0.1 * cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor= 1.2,
                                         minNeighbors= 5,
                                         minSize = (int(minW),int(minH)))

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 60:
            id = names[id]
        else:
            id = 'unknown'

        confidence  = "{0}%".format(round(100-confidence))

        cv2.putText(img, str(id), (x+5, y-5),font,1,(255,255,255),2)
        cv2.putText(img, str(confidence), (x+5, y+h-5), font,1,(255,255,0),1)

    cv2.imshow('camera', img)
    if cv2.waitKey(1)>0: break
print("\n [INFO] Exiting Program")
cam.release()
cv2.destroyAllWindows()