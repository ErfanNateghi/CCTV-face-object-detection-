from customtkinter import *
from CCTV import *
from tkinter import filedialog , Label ,PhotoImage, Canvas
from PIL import Image , ImageTk
import CTkListbox


default_image_path = None

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

def update_face_detection(value):
    CCTV.face_detection = value

def update_object_detection(value):
    CCTV.object_detection = value

def update_face_detection_image(value):
    image_sc.face_detection = value

def update_object_detection_image(value):
    image_sc.object_detection = value

def insert_image(no_image_size):
    global default_image_path
    default_image_path = filedialog.askopenfilename(initialdir="/", title="Select an image",
                                           filetypes=( [("Image Files", "*.jpg; *.png")]))
    if default_image_path != None:
        image_label_insert.configure(image=CTkImage(Image.open(default_image_path),size=(no_image_size[0],no_image_size[1])))

def image_save():
    final_image_save_path = filedialog.asksaveasfile(mode='w', defaultextension=".png",filetypes=(("JPEG file", "*.jpg"),("PNG file", "*.png"),("All Files", "*.*")),title="Where do you want to save your image?")

    if final_image_save_path != None:
        image_sc.save_image(final_image_save_path)


root = CTk()
root.geometry('1920x1080')
root.minsize(800, 600)
root.title("CCTV AI")

img_empty_camera = CTkImage(Image.open('emptyCamera3.png'),size=(root.winfo_width()*2,root.winfo_width()*1.5))
no_image = CTkImage(Image.open('noImage.jpg'),size=(root.winfo_width()*3,root.winfo_width()*2.25))
no_image_size = (root.winfo_width()*3,root.winfo_width()*2.25)


# create a notebook for tabs
tabControl = CTkTabview(root, width=1700,height=1000,corner_radius=50)
tabControl.pack(pady=20)

tab1 = tabControl.add('    CCTV    ')
tab2 = tabControl.add(' Image Scanner ')
tab3 = tabControl.add(' Add Person ')
tabControl._segmented_button.configure( height=50,font=('Arial',30))



# tab 1
#------------------------------------------------------------------------------------------------------------------------
# log and options frame
option_and_log_frame = CTkFrame(tab1,fg_color='#1B1B1B',width=400, height=500)
option_and_log_frame.pack(fill="both", side='right')

log_textbox = CTkTextbox(option_and_log_frame, width=300, height=400)
log_textbox.pack(anchor='s', padx=30, pady=30 )

update_log_button = CTkButton(option_and_log_frame, text='Update Log', command=update_log,font=('',30),width=200,height=50,corner_radius=20)
update_log_button.pack(pady=20)
# -------------------

# when checkbox is checked then face detection is enabled
checkbox_face_detection = CTkCheckBox(option_and_log_frame, text='Face Detection', font=('', 30), variable=BooleanVar(value=True))
checkbox_face_detection.configure(command=lambda: update_face_detection(checkbox_face_detection.get()))
checkbox_face_detection.pack(pady=40)
checkbox_object_detection = CTkCheckBox(option_and_log_frame,text='Object Detection',font=('',30), variable=BooleanVar(value=True))
checkbox_object_detection.configure(command=lambda: update_object_detection(checkbox_object_detection.get()))
checkbox_object_detection.pack(pady=40)


# frame for video
video_frame = CTkFrame(tab1)
video_frame.pack(fill="both", side='left', padx=50, pady=50)

video_label = []
# label for displaying video
video_label.append(CTkLabel(video_frame, text=''))
video_label[0].grid(row=0 , column= 0, padx=50, pady=50)
video_label.append(CTkLabel(video_frame, text=''))
video_label[1].grid(row=0 , column= 1, padx=50, pady=50)
video_label.append(CTkLabel(video_frame, text=''))
video_label[2].grid(row=1 , column= 0, padx=50, pady=50)
video_label.append(CTkLabel(video_frame, text=''))
video_label[3].grid(row=1 , column= 1, padx=50, pady=50)

#------------------------------------------------------------------------------------------------------------------------

#tab2
#------------------------------------------------------------------------------------------------------------------------
# split the tab into two (insert image and scan image)
insert_image_frame = CTkFrame(tab2 , bg_color='#2B2B2B', fg_color='#1B1B1B',corner_radius=50)
insert_image_frame.pack(fill="both",expand=True, side='left',padx=30, pady=30)

scan_image_frame = CTkFrame(tab2, bg_color='#2B2B2B', fg_color='#1B1B1B',corner_radius=50)
scan_image_frame.pack(fill="both",expand=True , side='right',padx=30, pady=30)
# a lable which will display the addressed image
image_label_insert = CTkLabel(insert_image_frame, text='',image=no_image)
image_label_insert.pack(fill="both",pady=50, side='top')
image_label_scan = CTkLabel(scan_image_frame, text='',image=no_image)
image_label_scan.pack(fill="both", pady=50, side='top')


# split the frame into two (insert button and scan options)
insert_button_frame = CTkFrame(insert_image_frame,fg_color='#1B1B1B')
insert_button_frame.pack(padx=30,anchor="s", fill="both",expand=True , side='left')

scan_options_frame = CTkFrame(insert_image_frame,fg_color='#1B1B1B')
scan_options_frame.pack( padx=30,anchor="s",fill='both',expand=True, side='right')

# button for insert image
insert_button = CTkButton(insert_button_frame, text='Insert Image', font=('', 30), width=200, height=50, corner_radius=20,command=lambda: insert_image(no_image_size))
insert_button.pack(pady=40)
# 2 switch for scan mode (face and object detection)
face_detection_switch = CTkSwitch(scan_options_frame, text='Face Detection', font=('', 30), variable=BooleanVar(value=True),command=lambda: update_face_detection_image(face_detection_switch.get()))
face_detection_switch.pack(pady=40 , anchor='w')
object_detection_switch = CTkSwitch(scan_options_frame, text='Object Detection', font=('', 30), variable=BooleanVar(value=True),command=lambda: update_object_detection_image(object_detection_switch.get()))
object_detection_switch.pack(pady=(20,40),anchor='w')

# split the frame into two (scan button and scan image , image information listbox)
save_scan_frame = CTkFrame(scan_image_frame,fg_color='#1B1B1B')
save_scan_frame.pack(padx=30,anchor="s", fill="both",expand=True , side='left')

image_info_frame = CTkFrame(scan_image_frame,fg_color='#1B1B1B')
image_info_frame.pack( padx=30,anchor="s",fill='both',expand=True, side='right')

# button for scan image
scan_button = CTkButton(save_scan_frame, text='Scan Image', font=('', 30), width=200, height=50, corner_radius=20,command=lambda: image_sc.scan(default_image_path))
scan_button.pack(pady=20, anchor='center')
save_image_button = CTkButton(save_scan_frame, text='Save Image', font=('', 30), width=200, height=50, corner_radius=20,command=image_save)
save_image_button.pack(pady=20, anchor='center')

# list box for image information
people_frame = CTkFrame(image_info_frame,fg_color='#1B1B1B')
people_frame.pack(pady=20,padx=(0,10),anchor="s", fill="both",expand=True , side='left')
people_label = CTkLabel(people_frame, text='People Found', font=('', 20))
people_label.pack()
info_listbox_people = CTkListbox.CTkListbox(people_frame, width=100, height=400, font=('', 20), fg_color='#1B1B1B', bg_color='#1B1B1B')
info_listbox_people.pack(fill= 'both', expand=True)

objects_frame = CTkFrame(image_info_frame,fg_color='#1B1B1B')
objects_frame.pack(pady=20,anchor="s", fill="both",expand=True , side='right')
people_label = CTkLabel(objects_frame, text='Objects Found', font=('', 20))
people_label.pack()
info_listbox_objects = CTkListbox.CTkListbox(objects_frame, width=100, height=400, font=('', 20), fg_color='#1B1B1B', bg_color='#1B1B1B')
info_listbox_objects.pack( fill= 'both', expand=True)

#------------------------------------------------------------------------------------------------------------------------
# Create video instance and start video streaming
CCTV = video(root,video_label,checkbox_face_detection._variable.get(),checkbox_object_detection._variable.get())
CCTV.train()
CCTV.video_stream()

image_sc = image_scanner(root,image_label_scan,face_detection_switch._variable.get(),object_detection_switch._variable.get(),no_image_size,info_listbox_people,info_listbox_objects)




root.mainloop()





