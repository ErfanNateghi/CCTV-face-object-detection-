import cv2
from PIL import ImageTk, Image
import face_recognition
import os 
import numpy as np
import time
from customtkinter import *



class video:

    def __init__(self,root,video_label):
            self.root = root
            self.video_label = video_label
            self.namelist = []
            self.encodeList = []
            self.images = []
            self.frame_counter = 0
            self.facesCurFrame = []
            self.encodesCurFrame = []
            self.log_counter = 0
            self.last_log_time = time.time()-10
            self.img_empty_camera = ImageTk.PhotoImage(file='emptyCamera3.png')
            self.cap = [None]*3
            
    




    #listing images and names
    def train(self):
        path = 'people'
        list = os.listdir(path)
        for cl in list:
            curImg = cv2.imread(f'{path}/{cl}')
            self.images.append(curImg)
            self.namelist.append(os.path.splitext(cl)[0])

        #encoding all images
        for img in self.images:
            small_image = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
            img = cv2.cvtColor(small_image, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            self.encodeList.append(encode)
        names_and_encoded_images = dict(zip(self.namelist,self.encodeList))

   

    def detect_faces(self,frame,small_frame):
        # detect face every 10 frames so it takes less time to process
        if self.frame_counter % 10 == 0:
            self.frame_counter += 1
            # Convert frame to RGB for face detection
            RGB_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            self.facesCurFrame = face_recognition.face_locations(small_frame)
            self.encodesCurFrame = face_recognition.face_encodings(RGB_small_frame,self.facesCurFrame)
        else:
            self.frame_counter += 1
        for encodeFace,faceLocation in zip(self.encodesCurFrame,self.facesCurFrame):
            matches = face_recognition.compare_faces(self.encodeList,encodeFace)
            faceDis = face_recognition.face_distance(self.encodeList,encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = self.namelist[matchIndex].upper()
            else:
                name = 'UNKNOWN'
            #print(name)
            top, right, bottom, left = faceLocation
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            # save a line of log containing the name of the person and the time but every 10 seconds for each person
            current_time = time.time()
            
            if current_time - self.last_log_time > 10:
                    self.last_log_time = current_time
                # open the file in append mode
                    with open('log.txt', 'a') as f:
                        f.write(name + ' at ' + time.strftime("%H:%M:%S") + '\n')
                        f.close()



        
        
        return frame
        

    
    def update(self,i):
        ret, frame = self.cap[i].read()
        if ret:
            
            # make frames smaller so it takes less time to process
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Detect faces and draw frames around them
            frame_with_faces = self.detect_faces(frame,small_frame)
            

            # Convert OpenCV image to PIL format
            rgb_img = cv2.cvtColor(frame_with_faces, cv2.COLOR_BGR2RGB)
            
            pil_img = Image.fromarray(rgb_img)
            resized_img = pil_img.resize((480, 360), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(resized_img)
            # Update label with new image
            self.video_label[i].img = img_tk
            self.video_label[i].configure(image=img_tk)
            
        
            
        self.root.after(1,self.update,i)

    def video_stream(self):
        for i in range(3):
            self.cap[i] = cv2.VideoCapture(i)
            if not self.cap[i].isOpened():
                self.video_label[i].configure(image=self.img_empty_camera)
            self.update(i)
                

        
        
        
