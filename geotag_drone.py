from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from PIL import Image,ImageTk
import random
import bcrypt
import pickle
import platform
import geotag_drone_interface
import os
import subprocess

root1 = ''
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_object(object_name):
    with open(object_name, "rb") as file:
        my_depickler = pickle.Unpickler(file)
        data = my_depickler.load()
    return data

def save_object(obj, object_name):
    with open(object_name, "wb") as file:
        my_depickler = pickle.Pickler(file)
        my_depickler.dump(obj)

error_type = ""
error_message = ""
def show_error():
    global error_type, error_message
    messagebox.showerror(error_type, error_message)

def login():
    global psw,root1,error_type, error_message

    if psw.get() == mdp:
        try:
            os.mkdir(my_documents_path+"\\Geotag_Drone")
        except OSError:
            pass
        save_object(mdp,my_documents_path+"\\Geotag_Drone\\licence")
        root1.destroy()
        geotag_drone_interface.root_main()
    else :
        error_type = "MOT DE PASSE INCORRECTE"
        error_message = "Entrer le mot de passe correspondant au nom de votre ordinateur"
        show_error()
psw = ''
def show_login():
    global psw, root1
    root1 = Tk()
    root1.title('Géotagage Vérification')
    root1.geometry('720x320+320+200')

    root1.minsize(720,320)
    root1.maxsize(720,32)

    root1.iconbitmap(resource_path('geotag_drone.ico'))
    logo = Canvas(root1,width=720,height=180,bg='#fe8134')
    logo.place(relx=0,rely=0, anchor='w')
    font = Font(family='Liberation Serif', size=16)
    logo.create_text(340,160,text='AUTHENTIFICATION',fill='white',justify=CENTER,font=font,anchor='center')
    #image1 = Image.open("key.png")
    #photo1 = ImageTk.PhotoImage(image1)
    image2 = Image.open(resource_path("innovadrone.png"))
    photo2 = ImageTk.PhotoImage(image2)
    #logo.create_image(0, 93, image=photo1, anchor='nw')
    nom_ordi = platform.uname().node
    name_ordi = StringVar(root1,value=' '+nom_ordi +' ')

    label1 = Label(root1,text='COMPUTER NAME  :  ',fg='#000',justify=CENTER,font=Font(family='Liberation Serif', size=12),anchor='center')
    label1.place(relx=0.1850,rely=.42, anchor='w')

    label = Label(root1,textvariable=name_ordi,fg='#fe8134',justify=CENTER,font=Font(family='Liberation Serif', size=12),anchor='center')
    label.place(relx=0.4,rely=.42, anchor='w')

    password_cv = Canvas(root1,width=100,height=30,bg='#fe8134')
    password_cv.place(relx=0.1850,rely=0.58, anchor='w')
    password_cv.create_text(52,15,text='Mot de passe',fill='white',justify=CENTER,font=Font(family='Liberation Serif', size=10),anchor='center')
    psw = Entry(root1,bd=0,insertwidth=2,width=40,fg='#fe8134',font=Font(family='Liberation Serif', size=12),textvariable=StringVar(root1,value=''),takefocus=0)
    psw.place(relx=0.345,rely=.58, anchor='w')
    cv1 = Canvas(root1,width=366,height=2,bg='#fe8134x   ')
    cv1.place(relx=0.335,rely=0.62, anchor='w')

    loged = Button(root1,text='Login', bg='#fe8134', fg='#fff',activebackground="#fe8134",activeforeground ="#fff",command=login,anchor='center',font=Font(family='Liberation Serif', size=14),justify='center')
    loged.place(relx=0.48,rely=0.75, anchor='w')

    cvm = Canvas(root1,width=240,height=80)
    cvm.place(relx=0.66,rely=0.87, anchor='w')
    cvm.create_image(25, 30, image=photo2, anchor='nw')

    root1.mainloop()


#salt = load_object("salt")
#name = platform.uname().node
#test = bcrypt.hashpw(name.encode('utf-8'),salt)
#save_object(test,my_documents_path+"\\Geotag_Drone\\licence")

#licence = load_object(my_documents_path+"\\Geotag Drone\\licence")
my_documents_path = os.path.expanduser('~\Documents')
salt = load_object(resource_path("salt"))
name = platform.uname().node
mdp = bcrypt.hashpw(name.encode('utf-8'),salt).decode("utf-8")[29:]

try:
    licence = load_object(my_documents_path+"\\Geotag_Drone\\licence")
    if licence == mdp:
        geotag_drone_interface.root_main()
    else:

        cmd = "del "+my_documents_path+"\\Geotag_Drone\\licence"
        subprocess.call(cmd, shell = True)
        show_login()

except FileNotFoundError:
    show_login()
except EOFError:
    cmd = "del "+my_documents_path+"\\Geotag_Drone\\licence"
    subprocess.call(cmd, shell = True)
    show_login()
