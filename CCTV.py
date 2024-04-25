import cv2
from PIL import Image
import face_recognition
import os 
import numpy as np
import time
from customtkinter import *
from ultralytics import YOLO
import random
import pickle

YOLO_MODEL = None
DETECTION_COLORS = []
CLASS_LIST =[]
FINAL_IMAGE = None

class video:

    def __init__(self,root,video_label,face_detection,object_detection):
            self.root = root
            self.video_label = video_label
            self.face_detection = face_detection
            self.object_detection = object_detection
            self.namelist = []
            self.encodeList = []
            self.images = []
            self.frame_counter = 0
            self.frame_counter2 = 0
            self.facesCurFrame = []
            self.encodesCurFrame = []
            self.log_counter = 0
            self.last_log_time = time.time()-10
            self.img_empty_camera = Image.open('emptyCamera3.png')
            self.cap = [None]*4
            self.results = None
            self.res = None
            self.names_and_encoded_images = {}
            
    #listing images and names
    def train(self):
        global YOLO_MODEL
        global DETECTION_COLORS
        global CLASS_LIST

        # loading images if they are not already loaded in encoding.pkl
        try:
            with open('encodings.pkl', 'rb') as f:
                self.names_and_encoded_images = pickle.load(f)
        except FileNotFoundError:
            self.names_and_encoded_images = {}
        path = 'people'
        list = os.listdir(path)
        for cl in list:
            curImg = cv2.imread(f'{path}/{cl}')
            name = os.path.splitext(cl)[0]
            self.images.append(curImg)
            if os.path.splitext(cl)[0] in self.names_and_encoded_images.keys(): # if in encoding.pkl skip the encoding
                self.namelist.append(name)
                self.encodeList.append(self.names_and_encoded_images[os.path.splitext(cl)[0]][0])
                self.names_and_encoded_images[os.path.splitext(cl)[0]][1] = True
            else: # if not in encoding.pkl encode the image
                self.namelist.append(name)
                small_image = cv2.resize(curImg, (0, 0), fx=0.25, fy=0.25)
                img = cv2.cvtColor(small_image, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                self.encodeList.append(encode)
                self.names_and_encoded_images[name] = [encode,True,time.time()]

        # make a copy of dic to remove false flags
        updated_names_and_encoded_images = {name:[encode,flag,last_seen] for (name, [encode, flag, last_seen]) in self.names_and_encoded_images.items() if flag == True}
        for name in updated_names_and_encoded_images.keys():
            updated_names_and_encoded_images[name][1] = False # initialize flag to false
        # Save encodings and names to a file for later use
        with open('encodings.pkl', 'wb') as f:
            pickle.dump(updated_names_and_encoded_images, f)


        # Load YOLOv8 model
        my_file = open("object_list/objects.txt", "r")
        data = my_file.read()
        CLASS_LIST = data.split("\n")
        my_file.close()
        YOLO_MODEL = YOLO('yolov8n.pt')
        DETECTION_COLORS = []
        for i in range(len(CLASS_LIST)):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            DETECTION_COLORS.append((b, g, r))
        
    def detect_objects(self, frame):
        
        # for better performance it can be change to 2 so that it detects objects in every 2nd frame
        if self.frame_counter2 % 1 == 0:
            # Get detected objects and their bounding boxes
            self.results = YOLO_MODEL.predict(source=[frame], conf=0.45, save=False)
            self.res = self.results[0].numpy()
            
                

            self.frame_counter2 += 1
        else:
            self.frame_counter2 += 1

        if len(self.res) != 0:
                for i in range(len(self.results[0])):

                    boxes = self.results[0].boxes
                    box = boxes[i]  # returns one box
                    objectID = box.cls.numpy()[0]
                    conf = box.conf.numpy()[0]
                    bb = box.xyxy.numpy()[0]

                    cv2.rectangle(frame,
                        (int(bb[0]), int(bb[1])),
                        (int(bb[2]), int(bb[3])),
                        DETECTION_COLORS[int(objectID)],3,)

            # Display class name and confidence
                    font = cv2.FONT_HERSHEY_COMPLEX
                    cv2.putText(frame,
                        CLASS_LIST[int(objectID)] + " " + str(round(conf, 3)) + "%",
                        (int(bb[0]), int(bb[1]) - 10),
                        font,1,(255, 255, 255),2,
                    )
        return frame

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
                name = self.namelist[matchIndex]
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
            # for every name there is a last_seen value which shows the last date the person was seen
            # we use this to check if the person has been seen in the last 10 seconds so that we can save a line of log
            if name == 'UNKNOWN':
                if current_time - self.last_log_time > 10:
                        self.last_log_time = current_time
                    # open the file in append mode
                        with open('log.txt', 'a') as f:
                            f.write(f'{name} at {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
                            f.close()
            else:
                if self.names_and_encoded_images[name][2] < current_time - 10:
                    self.names_and_encoded_images[name][2] = current_time
                    # open the file in append mode
                    with open('log.txt', 'a') as f:
                        f.write(f'{name} at {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
                        f.close()



        
        
        return frame
        
    def update(self):
        for i in range(4):
            if self.cap[i].isOpened():
                ret, frame = self.cap[i].read()
                if ret:
                    
                    # make frames smaller so it takes less time to process
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    
                    # Detect faces and draw frames around them
                    if self.face_detection:
                        frame_with_faces_object = self.detect_faces(frame,small_frame)
                    else:
                        frame_with_faces_object = frame

                    if self.object_detection:
                        frame_with_faces_object = self.detect_objects(frame_with_faces_object)
                    else:
                        pass
                    

                    # Convert OpenCV image to PIL format
                    rgb_img = cv2.cvtColor(frame_with_faces_object, cv2.COLOR_BGR2RGB)
                    
                    pil_img = Image.fromarray(rgb_img)
                    
                    img_tk = CTkImage(pil_img, size=(self.root.winfo_width()/4.5, self.root.winfo_height()/3.5))
                    # Update label with new image
                    self.video_label[i].img = img_tk
                    self.video_label[i].configure(image=img_tk)
            else:
                self.video_label[i].configure(image= CTkImage(Image.open('emptyCamera3.png'),size=(self.root.winfo_width()/4.5, self.root.winfo_height()/3.5)))
            
        self.root.after(1,self.update)



    def video_stream(self):
        for i in range(4):
            self.cap[i] = cv2.VideoCapture(i)
        self.update()

            

class image_scanner:
    def __init__(self,root,scanner_label,face_detection,object_detection,image_size,info_listbox_people,info_listbox_objects):
        self.root = root
        self.scanner_label = scanner_label
        self.default_image = None
        self.face_detection = face_detection
        self.object_detection = object_detection
        try:
            with open('encodings.pkl', 'rb') as f:
                self.names_and_encoded_images = pickle.load(f)
        except FileNotFoundError:
            self.names_and_encoded_images = {}
        self.image_size = image_size
        self.info_listbox_people = info_listbox_people
        self.info_listbox_objects = info_listbox_objects



    # scan for faces
    def detect_faces(self,default_image_RGB, small_image):
        faceloc = face_recognition.face_locations(small_image)
        encode = face_recognition.face_encodings(small_image,faceloc)
        for face_encoding, face_location,i in zip(encode, faceloc,range(len(faceloc))):
            list_of_encodings = [value[0] for key, value in self.names_and_encoded_images.items()]
            list_of_names = [key for key, value in self.names_and_encoded_images.items()]
            matches = face_recognition.compare_faces(list_of_encodings,face_encoding)
            faceDis = face_recognition.face_distance(list_of_encodings,face_encoding)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = list_of_names[matchIndex]
            else:
                name = 'UNKNOWN'

            self.info_listbox_people.insert(i,name)# insert into listbox
            # draw rectangle and name on image
            top, right, bottom, left = face_location
            top , right, bottom, left = top*4, right*4, bottom*4, left*4
            cv2.rectangle(default_image_RGB, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.putText(default_image_RGB, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 3, (36, 255, 12), 2)
        return default_image_RGB

    def detect_objects(self,image_with_faces):
        results = YOLO_MODEL.predict(source=[image_with_faces], conf=0.45, save=False)
        isResult = results[0].numpy() 

        if len(isResult) != 0:
                for i in range(len(results[0])):

                    boxes = results[0].boxes
                    box = boxes[i]  # returns one box
                    objectID = box.cls.numpy()[0]
                    conf = box.conf.numpy()[0]
                    bb = box.xyxy.numpy()[0]
                    
                    cv2.rectangle(image_with_faces,# draw rectangle
                        (int(bb[0]), int(bb[1])),
                        (int(bb[2]), int(bb[3])),
                        DETECTION_COLORS[int(objectID)],3,)
                    
                   

                    # Display class name and confidence
                    font = cv2.FONT_HERSHEY_COMPLEX
                    cv2.putText(image_with_faces,
                        CLASS_LIST[int(objectID)] + " " + str(round(conf, 3)) + "%",
                        (int(bb[0]), int(bb[1]) - 10),
                        font,3,(255, 255, 255),2,
                    )

                    self.info_listbox_objects.insert(i,CLASS_LIST[int(objectID)]) # insert name of object in listbox
                    


        return image_with_faces
    

    def save_image(self,path):
        if FINAL_IMAGE != None:
            FINAL_IMAGE.save(path)
    


    def scan(self,default_image_path):
        global FINAL_IMAGE
        # clear listboxs
        self.info_listbox_people.delete(0,'end')
        self.info_listbox_objects.delete(0,'end')
        # load and convert image to rgb
        default_image = cv2.imread(default_image_path)
        default_image_RGB = cv2.cvtColor(default_image, cv2.COLOR_BGR2RGB)
        # resize image for better speed
        small_image = cv2.resize(default_image_RGB, (0, 0), fx=0.25, fy=0.25)

        # scan image
        if self.face_detection:
            image_with_faces_object = self.detect_faces(default_image_RGB,small_image)
        else:
            image_with_faces_object = default_image_RGB
        if self.object_detection:
            image_with_faces_object = self.detect_objects(image_with_faces_object)
        
        # convert numpy array to PIL image
        pil_image = Image.fromarray(image_with_faces_object)
        # convert PIL image to ctk image
        img_ctk = CTkImage(pil_image, size=(self.image_size[0],self.image_size[1]))
        self.scanner_label.configure(image=img_ctk)

        FINAL_IMAGE = pil_image

        

