from PIL import ImageTk
from customtkinter import *
from face_recognition_functions import *
import threading

def update_log():
    try:
        log_textbox.delete(1.0, END)

        file = open('log.txt', 'r')
        file_text = reversed(file.readlines())
        log_textbox.insert(1.0, "".join(file_text))
    except Exception:
        print('error', 'something went wrong')

    finally:
        file.close()





root = CTk()
root.geometry('1800x1100')
root.title("CCTV AI")

img_empty_camera = ImageTk.PhotoImage(file='emptyCamera3.png')


# create a notebook for tabs
tabControl = CTkTabview(root, width=1700,height=1000,corner_radius=20)
tabControl.pack(pady=20)

tab1 = tabControl.add('    CCTV    ')
tab2 = tabControl.add('   IMAGEs   ')
tab3 = tabControl.add(' ADD PERSON ')
tabControl._segmented_button.configure( height=50,font=('Arial',30))

# log and options frame
option_and_log_frame = CTkFrame(tab1,fg_color='#1B1B1B',width=400, height=500)
option_and_log_frame.pack(fill="both", side='right')

log_textbox = CTkTextbox(option_and_log_frame, width=300, height=400)
log_textbox.pack(anchor='s', padx=30, pady=30)

update_log_button = CTkButton(option_and_log_frame, text='Update Log', command=update_log,font=('',30),width=200,height=50,corner_radius=20)
update_log_button.pack(pady=20)
# -------------------

checkbox_face_detection = CTkCheckBox(option_and_log_frame,text='Face Detection',font=('',30))
checkbox_face_detection.pack(pady=40)
checkbox_object_detection = CTkCheckBox(option_and_log_frame,text='Object Detection',font=('',30))
checkbox_object_detection.pack(pady=40)


# frame for video
video_frame = CTkFrame(tab1)
video_frame.pack(fill="both", side='left', padx=50, pady=50,)

video_label = []
# label for displaying video
video_label.append(CTkLabel(video_frame, text=''))
video_label[0].grid(row=0 , column= 0, padx=50, pady=50)
video_label[0].configure(image=img_empty_camera)
video_label.append(CTkLabel(video_frame, text=''))
video_label[1].grid(row=0 , column= 1, padx=50, pady=50)
video_label[1].configure(image=img_empty_camera)
video_label.append(CTkLabel(video_frame, text=''))
video_label[2].grid(row=1 , column= 0, padx=50, pady=50)
video_label[2].configure(image=img_empty_camera)
video_label.append(CTkLabel(video_frame, text=''))
video_label[3].grid(row=1 , column= 1, padx=50, pady=50)
video_label[3].configure(image=img_empty_camera)

# Start video streaming
facedetector = video(root=root,video_label=video_label)
facedetector.train()
#make a thread for video streaming
thread_video = threading.Thread(target=facedetector.video_stream, daemon=True)
thread_video.start()


root.mainloop()





