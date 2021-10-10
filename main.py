from tkinter import * # pip install tkinter
from tkinter.ttk import Progressbar
import imageio # pip install imageio
from PIL import ImageTk, Image # pip install pillow
#import tkFileDialog
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showerror, askyesno, showinfo
import moviepy.editor as mp  # pip install moviepy
import pygame # pip install pygame
import os
from threading import Thread
import time
from translate import translate
from SpeechToText import silence_based_conversion
import socket


pygame.mixer.init()
video_path = ''
sound_status = 'unmute'
progress_meter = 0
pause = False
count_upload = 0

def check_internet():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


def coversion_thread():
    global translate_button, progress, thread, thread1, prograess_label, thread1, thread, count_upload
    count_upload += 1
    if not check_internet():
        showerror("VDNotes", "Please connect internet!")
        return
    # Label(win, text="Translation is in progress: ", font=("Verdana", 15), bg="skyblue").place(x=10, y=600)
    thread = Thread(target=conversion)
    thread1=Thread(target=progress_bar)
    prograess_label = Label(win, text="Translation is in progress: ", font=("Verdana", 15), bg="skyblue")
    # thread.setDaemon(True)
    thread.start()
    prograess_label.place(x=10, y=592)
    translate_button.config(state=DISABLED)
    # thread1.setDaemon(True)
    thread1.start()
    return
        

def conversion():
    global language_entry, pause, progress_meter, progress
    pause = True
    pygame.mixer.music.unload()
    language = language_entry.get()
    try:
        respns = silence_based_conversion(r"data\\audio.wav")
    except:
        showerror("VDNotes", "There is an error try again!")
        translate_button.config(state=ACTIVE)
        progress['value'] = 0
        win.destroy()
        return 0
        
    try:
        text = open("recognized.txt", "r")
        textfile = open("text.txt", "w+", encoding="utf-8")
        for i in text:
            textfile.write(translate(i, language))
        textfile.close()

    except:
        showerror("VDNotes ", "There is an error try again!")
        translate_button.config(state=ACTIVE)
        win.destroy()
        return 0

    print("Translation Done")
    progress_meter = 100
    for i in range(75,101):
        progress['value'] = i
        win.update_idletasks() 
        time.sleep(0.5)
        win.update_idletasks()
    save_button.config(state=ACTIVE)
    showinfo("VDNotes", "Translation done, now you can save your notes.")
    language_entry.delete(0, END)
    prograess_label.destroy()
    progress.destroy()
    return


def file_save():
    files = [('Text Document', '*.txt')] 
    f = asksaveasfile(mode='w',filetypes = files, defaultextension = files) 
    # print(f)
    f = open(f.name, "w", encoding="utf-8")
    #f = asksaveasfile(mode='w', defaultextension=('Text Document', '*.txt'), filetypes=('Text Document', '*.txt'))
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return

    text2save = open("text.txt", "r", encoding="utf-8")
    try:
        for i in text2save:
            f.write(i)
        f.close()
        text2save.close()
        showinfo("VDNotes", "Notes are successfully saved.")
    except:
        showerror("VDNotes", "There is an error. Try again...")


def progress_bar():
    global progress_meter, progress
    progress = Progressbar(win, orient = HORIZONTAL, 
              length = 300, mode = 'determinate')
    progress.place(x=295, y=600)
    for i in range(75):
        if progress_meter == 100:
            progress["value"] = 100
            return
        progress['value'] = i
        win.update_idletasks() 
        time.sleep(1)
    return 
  

def sound_control():
    global sound_status
    #unmute_button.config(image=mute_button_img)
    if sound_status == "unmute":
        #print("yes")
        unmute_button.config(image=mute_button_img)
        pygame.mixer.music.set_volume(0)
        sound_status = "mute"
        unmute_label.config(text="Sound: OFF")
        return
    if sound_status == "mute":
        unmute_button.config(image=unmute_button_img)
        pygame.mixer.music.set_volume(0.99)
        sound_status = "unmute"
        unmute_label.config(text="Sound: ON")
        return



def video_to_audio(): 
    pygame.mixer.music.unload()
    clip = mp.VideoFileClip(video_path) 
    open("data/audio.wav", "wb")
    clip.audio.write_audiofile(r"data/audio.wav")


def play_music():
    pygame.mixer.music.load(r"data\\audio.wav")
    pygame.mixer.music.play()

def upload():
    global video_path, thread1, thread, prograess_label, progress,pause, count_upload
    pause=False
    save_button.config(state=DISABLED)
    upload_button.config(text="Please wait", state=DISABLED)
    if count_upload > 0:
        progress['value'] = 0
        win.update_idletasks()
        if thread1.is_alive() or thread.is_alive():
            showerror("VDNotes", "There is another translation running, Please wait...")
            upload_button.config(state=ACTIVE, text="Upload")
            return
        else:
            prograess_label.destroy()
            progress.destroy()

    video_path = askopenfilename(initialdir = "\\",title = "Select file",filetypes = (("mp4 files","*.mp4"),("wmv files","*.wmv"),("all files","*.*")))
    if video_path == '':
        upload_button.config(text="Uplaod", state=ACTIVE)
        return
    translate_button.config(state=ACTIVE)
    unmute_button.config(state=ACTIVE)
    title = video_path[video_path.rfind("/")+1:]
    print(title)
    if len(title) < 56:
        video_title.config(text="Video Title: "+title)
    else:
        video_title.config(text="Video Title: "+title[:55]+"...")
    video_to_audio()
    upload_button.config(text="Upload", state=ACTIVE)
    return video_frame(video_path)

def video_frame(path):
    global vid_frame, pause
    play_music()
    vid_frame.destroy()
    vid_frame = Frame(win, height=350, width=600, cursor="arrow", bg="black", highlightbackground="white", highlightcolor="white", highlightthickness=3)
    video_name = path
    video = imageio.get_reader(video_name)
    delay = int(1000 / video.get_meta_data()['fps'])
    vid_frame.place(x=125,y=10)
    def stream(label):

        try:
            image = video.get_next_data()
        except:
            video.close()
            return
        if pause == True:
            #pause = False
            return
        label.after(delay, lambda: stream(label))
        image = Image.fromarray(image)
        w, h = image.size
        if w>600 and h>350:
            image = image.resize((600,350), Image.ANTIALIAS)
        frame_image = ImageTk.PhotoImage(image)
        label.config(image=frame_image)
        label.image = frame_image
    my_label = Label(vid_frame, height=350, width=600)
    my_label.pack()
    my_label.after(delay, lambda: stream(my_label))



win = Tk()
win.geometry('850x650')
win.iconbitmap("data\\logo.ico")
win.title("VDNotes")
win.resizable(0, 0)
win['bg'] = "skyblue"

# Video player window
vid_frame = Frame(win, height=350, width=600, cursor="arrow", bg="black", highlightbackground="white", highlightcolor="white", highlightthickness=3)
vid_frame.place(x=125,y=10)

# button used to upload video
upload_button = Button(win, text="Upload", font=("Verdana", 15), cursor="hand2", width=15, command=upload)
upload_button.place(x=10, y=420)

# mute button
mute_button_img = Image.open('data\\mute.png')
mute_button_img = mute_button_img.resize((50,50), Image.ANTIALIAS)
mute_button_img = ImageTk.PhotoImage(mute_button_img)
# mute_button = Button(image=mute_button_img, bg="skyblue", relief=FLAT, activebackground='skyblue', command=sound_control)
# mute_button.place(x=750, y=15)

# unmute button
unmute_button_img = Image.open('data\\speaker.png')
unmute_button_img = unmute_button_img.resize((50,50), Image.ANTIALIAS)
unmute_button_img = ImageTk.PhotoImage(unmute_button_img)
unmute_button = Button(win,bg="skyblue", relief=FLAT, activebackground='skyblue', command = sound_control, state=DISABLED, cursor="hand2")
unmute_button.config(image=unmute_button_img)
unmute_button.place(x=750, y=15)

# sound on label
unmute_label = Label(win, text="Sound: ON", bg = "skyblue", font=("Verdana", 10))
unmute_label.place(x=745, y=80)


# video title
video_title = Label(win, text="Video Title: ", font=("Verdana", 15), bg="skyblue")
video_title.place(x=10, y=380)


# language entry label
language_label = Label(win, text="Enter translation language: ", font=("Verdana", 15), bg="skyblue")
language_label.place(x=10, y=470)

# language entry 
language_entry = Entry(win, width=15, border=1, font=("Verdana", 15))
language_entry.place(x=300, y=474)


# translate button
translate_button = Button(win, text="Translate", font=("Verdana", 15), cursor="hand2", width=15, state=DISABLED, command=coversion_thread)
translate_button.place(x=298, y=520)

prograess_label = Label(win, text="Translation is in progress: ", font=("Verdana", 15), bg="skyblue")
progress = Progressbar(win, orient = HORIZONTAL, 
              length = 300, mode = 'determinate')

# save button
save_button = Button(win, text="save", font=("Verdana", 15), cursor="hand2", state=DISABLED, width=10, command= file_save)
save_button.place(x=680, y=420)

# save file label
save_label = Label(win, text="Save file:", font=("Verdana", 15), bg="skyblue")
save_label.place(x=560, y=423)


win.mainloop()