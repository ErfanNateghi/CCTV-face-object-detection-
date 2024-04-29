from customtkinter import *
from CCTV import *
from tkinter import filedialog
from PIL import Image
import CTkListbox
import shutil
from tkinter import messagebox


default_image_path = None
window_width = None
window_height = None
first_Loop = True



def center_window(root,window_width,window_height):
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')


def GUI_APP():
    global window_width
    global window_height
    global first_Loop

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
        person_label.configure(image=CTkImage(Image.open(image_path),size=(window_width/4.8,window_height/3.6)))
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
        person_label.configure(image=CTkImage(Image.open(image_path),size=(window_width/4.8,window_height/3.6)))
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
            person_label.configure(image=CTkImage(Image.open('noImage.jpg'),size=(window_width/4.8,window_height/3.6)))
            # delete the image file in the people folder
            image_name = name + '.jpg'
            os.remove('people/' + image_name)
        except Exception:
            messagebox.showerror("Error", "There is no person with this name")

    def change_display_size(size):
        
        global window_width,window_height    
        if size != 'full screen':
            window_width = int(size.split('x')[0])
            window_height = int(size.split('x')[1])
        else:
            window_width = root.winfo_screenwidth()
            window_height = root.winfo_screenheight()
        root.destroy()
        GUI_APP()# refresh the page so widgets update

 #------------------------------------------------------------------------------------------------------------------------
    root = CTk()
    if first_Loop:
        window_width = root.winfo_screenwidth()
        window_height = root.winfo_screenheight()
        first_Loop = False
    center_window(root,window_width,window_height)
    root.resizable(False,False)
    root.title("CCTV AI")



    img_empty_camera = CTkImage(Image.open('emptyCamera3.png'),size=(window_width/4.8,window_height/3.6))
    no_image = CTkImage(Image.open('noImage.jpg'),size=(window_width/3.2,window_height/2.4))
    no_image_size = (window_width/3.2,window_height/2.4)
    no_image_tab3 = CTkImage(Image.open('noImage.jpg'),size=(window_width/4.8,window_height/3.6))



    # create a notebook for tabs
    tabControl = CTkTabview(root, width=window_width/1.13,height=window_height/1.08,corner_radius=window_width/38.4)
    tabControl.pack(pady=window_height/54)

    tab1 = tabControl.add('    CCTV    ')
    tab2 = tabControl.add(' Image Scanner ')
    tab3 = tabControl.add(' Add Person ')
    tab4 = tabControl.add(' display settings ')
    tab5 = tabControl.add(' About ')
    tabControl._segmented_button.configure( height=window_height/21.6,font=('Arial',window_width/64))



    # tab 1
    #------------------------------------------------------------------------------------------------------------------------
    # log and options frame
    option_and_log_frame = CTkFrame(tab1,fg_color='#1B1B1B',width=window_width/4.8, height=window_height/2.16)
    option_and_log_frame.pack(fill="both", side='right')

    log_textbox = CTkTextbox(option_and_log_frame, width=window_width/6.4, height= window_height/2.7)
    log_textbox.pack(anchor='s', padx=window_width/64, pady=window_height/36 )

    update_log_button = CTkButton(option_and_log_frame, text='Update Log', command=update_log,font=('',window_width/64),width=window_width/9.6,height=window_height/21.6,corner_radius=window_width/96)
    update_log_button.pack(pady=window_height/54)
    # -------------------

    # when checkbox is checked then face detection is enabled
    checkbox_face_detection = CTkCheckBox(option_and_log_frame, text='Face Detection', font=('', window_width/64), variable=BooleanVar(value=True))
    checkbox_face_detection.configure(command=lambda: update_face_detection(checkbox_face_detection.get()))
    checkbox_face_detection.pack(pady=window_height/27)
    checkbox_object_detection = CTkCheckBox(option_and_log_frame,text='Object Detection',font=('',window_width/64), variable=BooleanVar(value=True))
    checkbox_object_detection.configure(command=lambda: update_object_detection(checkbox_object_detection.get()))
    checkbox_object_detection.pack(pady=window_height/27)


    # frame for video
    video_frame = CTkFrame(tab1)
    video_frame.pack(fill="both", side='left', padx=window_width/38.4, pady=window_height/21.6)

    video_label = []
    # label for displaying video
    video_label.append(CTkLabel(video_frame, text=''))
    video_label[0].grid(row=0 , column= 0, padx=window_width/38.4, pady=window_height/21.6)
    video_label.append(CTkLabel(video_frame, text=''))
    video_label[1].grid(row=0 , column= 1, padx=window_width/38.4, pady=window_height/21.6)
    video_label.append(CTkLabel(video_frame, text=''))
    video_label[2].grid(row=1 , column= 0, padx=window_width/38.4, pady=window_height/21.6)
    video_label.append(CTkLabel(video_frame, text=''))
    video_label[3].grid(row=1 , column= 1, padx=window_width/38.4, pady=window_height/21.6)

    #------------------------------------------------------------------------------------------------------------------------

    #tab2
    #------------------------------------------------------------------------------------------------------------------------
    # split the tab into two (insert image and scan image)
    insert_image_frame = CTkFrame(tab2 , bg_color='#2B2B2B', fg_color='#1B1B1B',corner_radius=window_width/38.4)
    insert_image_frame.pack(fill="both",expand=True, side='left',padx=window_width/64, pady=window_height/36)

    scan_image_frame = CTkFrame(tab2, bg_color='#2B2B2B', fg_color='#1B1B1B',corner_radius=window_width/38.4)
    scan_image_frame.pack(fill="both",expand=True , side='right',padx=window_width/64, pady=window_height/36)
    # a lable which will display the addressed image
    image_label_insert = CTkLabel(insert_image_frame, text='',image=no_image)
    image_label_insert.pack(fill="both",pady=window_height/21.6, side='top')
    image_label_scan = CTkLabel(scan_image_frame, text='',image=no_image)
    image_label_scan.pack(fill="both", pady=window_height/21.6, side='top')


    # split the frame into two (insert button and scan options)
    insert_button_frame = CTkFrame(insert_image_frame,fg_color='#1B1B1B')
    insert_button_frame.pack(padx=window_width/64,anchor="s", fill="both",expand=True , side='left')

    scan_options_frame = CTkFrame(insert_image_frame,fg_color='#1B1B1B')
    scan_options_frame.pack( padx=window_width/64,anchor="s",fill='both',expand=True, side='right')

    # button for insert image
    insert_button = CTkButton(insert_button_frame, text='Insert Image', font=('', window_width/64), width=window_width/9.6, height=window_height/21.6, corner_radius=window_width/96,command=lambda: insert_image(no_image_size))
    insert_button.pack(pady=window_height/27)
    # 2 switch for scan mode (face and object detection)
    face_detection_switch = CTkSwitch(scan_options_frame, text='Face Detection', font=('', window_width/64), variable=BooleanVar(value=True),command=lambda: update_face_detection_image(face_detection_switch.get()))
    face_detection_switch.pack(pady=window_height/27 , anchor='w')
    object_detection_switch = CTkSwitch(scan_options_frame, text='Object Detection', font=('', window_width/64), variable=BooleanVar(value=True),command=lambda: update_object_detection_image(object_detection_switch.get()))
    object_detection_switch.pack(pady=(window_height/54,window_height/27),anchor='w')

    # split the frame into two (scan button and scan image , image information listbox)
    save_scan_frame = CTkFrame(scan_image_frame,fg_color='#1B1B1B')
    save_scan_frame.pack(padx=window_width/64,anchor="s", fill="both",expand=True , side='left')

    image_info_frame = CTkFrame(scan_image_frame,fg_color='#1B1B1B')
    image_info_frame.pack( padx=window_width/64,anchor="s",fill='both',expand=True, side='right')

    # button for scan image
    scan_button = CTkButton(save_scan_frame, text='Scan Image', font=('', window_width/64), width=window_width/9.6, height=window_height/21.6, corner_radius=window_width/96,command=lambda: image_sc.scan(default_image_path))
    scan_button.pack(pady=window_height/54, anchor='center')
    save_image_button = CTkButton(save_scan_frame, text='Save Image', font=('', window_width/64), width=window_width/9.6, height=window_height/21.6, corner_radius=window_width/96,fg_color='green',command=image_save)
    save_image_button.pack(pady=window_height/54, anchor='center')

    # list box for image information
    people_frame = CTkFrame(image_info_frame,fg_color='#1B1B1B')
    people_frame.pack(pady=window_height/54,padx=(0,window_width/192),anchor="s", fill="both",expand=True , side='left')
    people_label = CTkLabel(people_frame, text='People Found', font=('', window_width/96))
    people_label.pack()
    info_listbox_people = CTkListbox.CTkListbox(people_frame, width=window_width/19.2, height=window_height/2.7, font=('', window_width/96), fg_color='#1B1B1B', bg_color='#1B1B1B')
    info_listbox_people.pack(fill= 'both', expand=True)

    objects_frame = CTkFrame(image_info_frame,fg_color='#1B1B1B')
    objects_frame.pack(pady=window_height/54,anchor="s", fill="both",expand=True , side='right')
    people_label = CTkLabel(objects_frame, text='Objects Found', font=('', window_width/96))
    people_label.pack()
    info_listbox_objects = CTkListbox.CTkListbox(objects_frame, width=window_width/19.2, height=window_height/2.7, font=('', window_width/96), fg_color='#1B1B1B', bg_color='#1B1B1B')
    info_listbox_objects.pack( fill= 'both', expand=True)


    # tab3 (add person and remove person)
    #------------------------------------------------------------------------------------------------------------------------
    main_add_person_frame = CTkFrame(tab3, bg_color='#2B2B2B', fg_color='#1B1B1B',corner_radius=window_width/38.4,width=window_width/1.6, height=window_height/1.35)
    main_add_person_frame.pack(padx=window_width/64, pady=window_height/36, anchor='center')
    # frame for image, add , remove
    image_add_remove_frame = CTkFrame(main_add_person_frame,fg_color='#1B1B1B')
    image_add_remove_frame.pack(side='left',padx=(window_width/38.4,0), pady=window_height/21.6)
    # label for showing the pendding person
    person_label = CTkLabel(image_add_remove_frame, text='', font=('', window_width/96) , width=window_width/4.8, height=window_height/4.32, corner_radius=window_width/96, image=no_image_tab3)
    person_label.pack(pady=window_height/54,padx=window_width/64, side='top')

    frame_add_delete_person = CTkFrame(image_add_remove_frame,fg_color='#1B1B1B')
    frame_add_delete_person.pack(pady=window_height/54,padx=window_width/64, anchor= 's', side='bottom')

    add_person_botton = CTkButton(frame_add_delete_person, text='Add Person', font=('', window_width/96), width=window_width/9.6, height=window_height/21.6, corner_radius=window_width/96,command=add_person, fg_color='green')
    add_person_botton.pack(pady=window_height/54,padx=window_width/64, side = 'right')

    delete_person_botton = CTkButton(frame_add_delete_person, text='Remove Person', font=('', window_width/96), width=window_width/9.6, height=window_height/21.6, corner_radius=window_width/96,command=remove_person, fg_color='red')
    delete_person_botton.pack(pady=window_height/54,padx=window_width/64, side = 'left')

    # frame for entering person first name and last name
    person_info_frame = CTkFrame(main_add_person_frame,fg_color='#1B1B1B')
    person_info_frame.pack(padx=(0,window_width/64),pady=window_height/21.6, fill="both",expand=True , side='right')
    # a label and entry for first name and last name plus a buttons for image path and a label for image path
    Fname_Lname_frame = CTkFrame(person_info_frame,fg_color='#1B1B1B')
    Fname_Lname_frame.pack(pady=window_height/54,anchor="center", side='left')

    first_name_label = CTkLabel(Fname_Lname_frame, text='First Name:', font=('', window_width/64))
    first_name_label.pack(pady=window_height/54,padx=window_width/64, anchor= 'w')
    first_name_entry = CTkEntry(Fname_Lname_frame, font=('', window_width/76.8),width=window_width/9.6,height=window_height/21.6)
    first_name_entry.pack(pady=(0,window_height/54),padx=window_width/64, anchor= 'w')

    last_name_label = CTkLabel(Fname_Lname_frame, text='Last Name:', font=('', window_width/64))
    last_name_label.pack(pady=window_height/54,padx=window_width/64, anchor= 'w')
    last_name_entry = CTkEntry(Fname_Lname_frame, font=('', window_width/76.8),width=window_width/9.6,height=window_height/21.6)
    last_name_entry.pack(pady=(0,window_height/54),padx=window_width/64, anchor= 'w')

    add_person_image_path_button = CTkButton(Fname_Lname_frame, text='Image Path', font=('', window_width/96), width=window_width/9.6, height=window_height/21.6, corner_radius=window_width/96,command=lambda: add_person_image_load())
    add_person_image_path_button.pack(pady=window_height/54,padx=window_width/64, anchor= 'w')
    add_person_image_path_label = CTkLabel(Fname_Lname_frame, text='', font=('', window_width/192),fg_color='#2B2B2B' ,width=window_width/4.8, height=window_height/21.6, corner_radius=window_width/96)
    add_person_image_path_label.pack(pady=(0,window_height/54),padx=window_width/64, anchor= 'w',expand=True)

    people_listbox = CTkListbox.CTkListbox(person_info_frame, width=window_width/9.6, height=window_height/2.7, font=('', window_width/64), fg_color='#1B1B1B', bg_color='#1B1B1B')
    people_listbox.pack(side='right')
    for i in os.listdir('people'):
        people_listbox.insert('end',i.split('.')[0])
    people_listbox.bind('<<ListboxSelect>>', select_person)


    # tab4 (display setting)
    #------------------------------------------------------------------------------------------------------------------------
    # make a frame for display setting
    display_main_frame = CTkFrame(tab4,fg_color='#1B1B1B')
    display_main_frame.pack(padx=(0,window_width/64),pady=window_height/21.6)
    # make a listbox for display different screen size
    display_size_listbox = CTkListbox.CTkListbox(display_main_frame,font=('',window_width/64),width=window_width/8, height=window_height/3)
    display_size_listbox.pack(padx=window_width/64,pady=window_height/21.6)
    display_size_listbox.insert('end','full screen')
    display_size_listbox.insert('end','3840x2160')
    display_size_listbox.insert('end','2560x1440')
    display_size_listbox.insert('end','1920x1080')
    display_size_listbox.insert('end','1680x1050')
    display_size_listbox.insert('end','1600x900')
    display_size_listbox.insert('end','1536x864')
    display_size_listbox.insert('end','1440x900')
    display_size_listbox.insert('end','1366x768')
    display_size_listbox.insert('end','1280x800')
    display_size_listbox.insert('end','1280x720')
    display_size_listbox.insert('end','1024x768')
    display_size_listbox.insert('end','800x600')
    display_size_listbox.insert('end','640x480')
    display_size_listbox.configure(font=('',window_width/64))
    # button for apply setting
    apply_button = CTkButton(display_main_frame, text='Apply', font=('', window_width/96), width=window_width/9.6, height=window_height/21.6, corner_radius=window_width/96,command=lambda: change_display_size(display_size_listbox.get(display_size_listbox.curselection())))
    apply_button.pack(pady=window_height/54)


    #------------------------------------------------------------------------------------------------------------------------

    # Create video instance and start video streaming
    CCTV = video(root,video_label,checkbox_face_detection._variable.get(),checkbox_object_detection._variable.get())
    CCTV.train()
    CCTV.video_stream()

    image_sc = image_scanner(root,image_label_scan,face_detection_switch._variable.get(),object_detection_switch._variable.get(),no_image_size,info_listbox_people,info_listbox_objects)




    root.mainloop()

if __name__ == '__main__':
    GUI_APP()
    
    


