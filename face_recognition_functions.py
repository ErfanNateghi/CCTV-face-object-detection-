import cv2
from PIL import ImageTk, Image
import face_recognition
import os , sys
import numpy
import math



class video:

    images = []
    classNames = []
    encodeList = []
    #listing images
    path = 'people'
    list = os.listdir(path)
    print(list)
    for cl in list:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    #encoding all images
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    

    def __init__(self,root,video_label):
        self.root = root
        self.video_label = video_label

    def detect_faces(self,frame):
        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Load pre-trained face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # Draw frames around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Person", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        return frame

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            # Detect faces and draw frames around them
            frame_with_faces = self.detect_faces(frame)
            # Convert OpenCV image to PIL format
            rgb_img = cv2.cvtColor(frame_with_faces, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_img)
            resized_img = pil_img.resize((480, 360), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(resized_img)
            # Update label with new image
            self.video_label[0].img = img_tk
            self.video_label[0].configure(image=img_tk)
        self.root.after(10, self.update)

    def video_stream(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Unable to open camera.")
            return
        
        
        
        self.update()
