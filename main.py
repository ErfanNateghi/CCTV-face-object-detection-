from customtkinter import *
from CCTV import *
from tkinter import filedialog
from PIL import Image
import CTkListbox
import shutil
from tkinter import messagebox


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

def add_person_image_load():
    image_path = filedialog.askopenfilename(initialdir="/", title="Select an image", filetypes=([("Image Files", "*.jpg; *.png")]))
    Image.open(image_path)
    person_label.configure(image=CTkImage(Image.open(image_path),size=(400,300)))
    add_person_image_path_label.configure(text=image_path)

def add_person():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    image_path = add_person_image_path_label._text
    if first_name != '' and last_name != '' and  image_path != '':
        # first letter of first name and last name should be uppercase
        name = first_name.capitalize() + ' ' + last_name.capitalize()
        # copy image from image path to people folder with their name
        image_name = name + '.jpg'
        shutil.copy(image_path, 'people/' + image_name)
        # update people listbox
        people_listbox.insert('end', name)

def select_person(event):
    person_name = event.widget.get(event.widget.curselection())
    first_name = person_name.split(' ')[0]
    last_name = person_name.split(' ')[1]
    image_path = 'people/' + person_name + '.jpg'
    person_label.configure(image=CTkImage(Image.open(image_path),size=(400,300)))
    add_person_image_path_label.configure(text=image_path)
    first_name_entry.delete(0, 'end')
    first_name_entry.insert(0, first_name)
    last_name_entry.delete(0, 'end')
    last_name_entry.insert(0, last_name)

def remove_person():
    name = first_name_entry.get() + ' ' + last_name_entry.get()
    
    try:
        # delete the item in the listbox with this name
        people_listbox.delete(people_listbox.get(ALL).index(name))
        # clear the entries
        first_name_entry.delete(0, 'end')
        last_name_entry.delete(0, 'end')
        person_label.configure(image=CTkImage(Image.open('noImage.jpg'),size=(400,300)))
        # delete the image file in the people folder
        image_name = name + '.jpg'
        os.remove('people/' + image_name)
    except Exception:
        messagebox.showerror("Error", "There is no person with this name")


window_width = 1920
window_height = 1080

root = CTk()
root.geometry(str(window_width) + 'x' + str(window_height))
root.minsize(800, 600)
root.title("CCTV AI")

print(root.winfo_width(), root.winfo_height())
img_empty_camera = CTkImage(Image.open('emptyCamera3.png'),size=(root.winfo_width()*2,root.winfo_width()*1.5))
no_image = CTkImage(Image.open('noImage.jpg'),size=(root.winfo_width()*3,root.winfo_width()*2.25))
no_image_size = (root.winfo_width()*3,root.winfo_width()*2.25)
no_image_tab3 = CTkImage(Image.open('noImage.jpg'),size=(root.winfo_width()*2,root.winfo_width()*1.5))



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


# tab3 (add person and remove person)
#------------------------------------------------------------------------------------------------------------------------
main_add_person_frame = CTkFrame(tab3, bg_color='#2B2B2B', fg_color='#1B1B1B',corner_radius=50,width=1200, height=800)
main_add_person_frame.pack(padx=30, pady=30, )
# frame for image, add , remove
image_add_remove_frame = CTkFrame(main_add_person_frame,fg_color='#1B1B1B')
image_add_remove_frame.pack(side='left',padx=(50,0), pady=50)
# label for showing the pendding person
person_label = CTkLabel(image_add_remove_frame, text='', font=('', 20) , width=400, height=250, corner_radius=20, image=no_image_tab3)
person_label.pack(pady=20,padx=30, side='top')

frame_add_delete_person = CTkFrame(image_add_remove_frame,fg_color='#1B1B1B')
frame_add_delete_person.pack(pady=20,padx=30, anchor= 's', side='bottom')

add_person_botton = CTkButton(frame_add_delete_person, text='Add Person', font=('', 20), width=200, height=50, corner_radius=20,command=add_person)
add_person_botton.pack(pady=20,padx=30, side = 'right')

delete_person_botton = CTkButton(frame_add_delete_person, text='Remove Person', font=('', 20), width=200, height=50, corner_radius=20,command=remove_person)
delete_person_botton.pack(pady=20,padx=30, side = 'left')

# frame for entering person first name and last name
person_info_frame = CTkFrame(main_add_person_frame,fg_color='#1B1B1B')
person_info_frame.pack(padx=(0,30),pady=50, fill="both",expand=True , side='right')
# a label and entry for first name and last name plus a buttons for image path and a label for image path
Fname_Lname_frame = CTkFrame(person_info_frame,fg_color='#1B1B1B')
Fname_Lname_frame.pack(pady=20,anchor="center", side='left')

first_name_label = CTkLabel(Fname_Lname_frame, text='First Name:', font=('', 30))
first_name_label.pack(pady=20,padx=30, anchor= 'w')
first_name_entry = CTkEntry(Fname_Lname_frame, font=('', 25),width=200,height=50)
first_name_entry.pack(pady=(0,20),padx=30, anchor= 'w')

last_name_label = CTkLabel(Fname_Lname_frame, text='Last Name:', font=('', 30))
last_name_label.pack(pady=20,padx=30, anchor= 'w')
last_name_entry = CTkEntry(Fname_Lname_frame, font=('', 25),width=200,height=50)
last_name_entry.pack(pady=(0,20),padx=30, anchor= 'w')

add_person_image_path_button = CTkButton(Fname_Lname_frame, text='Image Path', font=('', 20), width=200, height=50, corner_radius=20,command=lambda: add_person_image_load())
add_person_image_path_button.pack(pady=20,padx=30, anchor= 'w')
add_person_image_path_label = CTkLabel(Fname_Lname_frame, text='', font=('', 10),fg_color='#2B2B2B' ,width=400, height=50, corner_radius=20)
add_person_image_path_label.pack(pady=(0,20),padx=30, anchor= 'w',expand=True)

people_listbox = CTkListbox.CTkListbox(person_info_frame, width=200, height=400, font=('', 30), fg_color='#1B1B1B', bg_color='#1B1B1B')
people_listbox.pack(side='right')
for i in os.listdir('people'):
    people_listbox.insert('end',i.split('.')[0])
people_listbox.bind('<<ListboxSelect>>', select_person)
    


#------------------------------------------------------------------------------------------------------------------------

# Create video instance and start video streaming
CCTV = video(root,video_label,checkbox_face_detection._variable.get(),checkbox_object_detection._variable.get())
CCTV.train()
CCTV.video_stream()

image_sc = image_scanner(root,image_label_scan,face_detection_switch._variable.get(),object_detection_switch._variable.get(),no_image_size,info_listbox_people,info_listbox_objects)




root.mainloop()





