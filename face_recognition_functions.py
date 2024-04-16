import cv2
from PIL import ImageTk, Image
import tkinter as tk



class video:

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
            # Resize image to fit label
            resized_img = pil_img.resize((480, 360), Image.LANCZOS)
            # Convert PIL image to Tkinter PhotoImage
            img_tk = ImageTk.PhotoImage(resized_img)
            # Update label with new image
            self.video_label[0].img = img_tk
            self.video_label[0].configure(image=img_tk)
        self.root.after(10, self.update)

    def video_stream(self):
        # Open video stream (replace '0' with the index of your camera)
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Unable to open camera.")
            return
        
        
        
        # Start updating video feed
        self.update()
