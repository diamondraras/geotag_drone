import numpy as np
import subprocess
from geotag_functions import *
from decimal import Decimal
from tkinter.font import Font
from tkinter import ttk,messagebox,filedialog,Tk,sys,Canvas,CENTER,Label,StringVar,Button,LEFT,Radiobutton,Entry,IntVar
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
from os import path,mkdir
import matplotlib.pyplot as plt

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative_path)
    return path.join(path.abspath("."), relative_path)


fichierlog = ''
custom_path = ''
error_type = ''
error_message = ''
filelog = ''
folder_path = ''
type_epsg = ''
latence = 0
offsetx_gps = ''
offsety_gps = ''
offsetz_gps = ''
camx_gps = ''
camy_gps = ''
camz_gps = ''
x_gps = 0.0
y_gps = 0.0
z_gps = 0.0
x_cam = 0.0
y_cam = 0.0
z_cam = 0.0
epsg = 23031
offsetx_pivot1=''
offsety_pivot1=''
offsetz_pivot1=''
offsetx_pivot2=''
offsety_pivot2=''
offsetz_pivot2=''
base_init_x = ''
base_init_y = ''
base_init_z = ''
base_ppk_x = ''
base_ppk_y = ''
base_ppk_z = ''
valeur_angle_fixe = ''

message=''
type_message=''
#variable
def root_main():
    global message,type_message,offsetx_pivot1,offsety_pivot1,offsetz_pivot1,latence,offsetx_pivot2,offsety_pivot2,offsetz_pivot2,folder_path,filelog,error_type,error_message,custom_path,type_epsg,fichierlog, custom_path, error_type, error_message, valeur_angle_fixe

    #liste des fonction
    def OpenFile():
        global filelog,fichierlog
        name = askopenfilename(filetypes =(("Log File", "*.log"),("All Files","*.log")),title = "Choose a log file.")
        fichierlog = name
        if name!= '' :
            filelog.set(name)

    # def activate_gps():   
    #     offsetx_gps.config(state="normal")
    #     offsety_gps.config(state="normal")
    #     offsetz_gps.config(state="normal")
    #     print("activate_gps")

    # def desactivate_gps():
    #     offsetx_gps.config(state="disable")
    #     offsety_gps.config(state="disable")
    #     offsetz_gps.config(state="disable")
    #     print("desactivate_gps")

    def browse_button():
        global folder_path,custom_path
        filename = filedialog.askdirectory()
        custom_path = filename
        if filename!= '':
            folder_path.set(filename)

    def show_error():
        global error_type, error_message
        messagebox.showerror(error_type, error_message)

    def show_info():
        global message,type_message
        messagebox.showinfo(type_message,message)

    def activation_pivot():
        global offsetx_pivot1,offsety_pivot1,offsetz_pivot1,offsetx_pivot2,offsety_pivot2,offsetz_pivot2
        offsetx_pivot1.config(state='normal')
        offsety_pivot1.config(state='normal')
        offsetz_pivot1.config(state='normal')
        offsetx_pivot2.config(state='normal')
        offsety_pivot2.config(state='normal')
        offsetz_pivot2.config(state='normal')

    def desactivation_pivot():
        global offsetx_pivot1,offsety_pivot1,offsetz_pivot1,offsetx_pivot2,offsety_pivot2,offsetz_pivot2
        offsetx_pivot1.config(state='disable')
        offsety_pivot1.config(state='disable')
        offsetz_pivot1.config(state='disable')
        offsetx_pivot2.config(state='disable')
        offsety_pivot2.config(state='disable')
        offsetz_pivot2.config(state='disable')
        
    def nacelle_fixe():
        global valeur_angle_fixe
        valeur_angle_fixe.config(state="normal")

    def nacelle_mobile():
        global valeur_angle_fixe
        valeur_angle_fixe.config(state="disable")


    def help_button():
        global message,type_message
        message = str("Offset x + vers l'avant en mètre.\nOffset y + vers la droite en mètre.\nOffset z + vers le haut en mètre.")
        type_message = 'AIDE'
        show_info()

    def process_button():

        global error_type,error_message,x_gps,y_gps,z_gps,x_cam,y_cam,z_cam,epsg,message, type_message

        if fichierlog == '':
            error_type = 'ERREUR DE FICHIER'
            error_message = 'Aucun fichier choisi'
            show_error()
        elif custom_path == '':
            error_type = 'ERREUR DE DOSSIER'
            error_message = 'Aucun dossier destination choisi'
            show_error()
        elif type_epsg.get()=='':
            error_type = 'VALEUR EPSG INCORRECTE'
            error_message = 'Entrer une valeur entière'
            show_error()
        elif latence.get()=='':
            error_type = 'VALEUR LATENCE INCORRECTE'
            error_message = 'Entrer une valeur entière'
            show_error()
            
        else:
            try:
                x_gps = float(offsetx_gps.get())
                y_gps = float(offsety_gps.get())
                z_gps = float(offsetz_gps.get())
                x_cam = float(offsetx_cam.get())
                y_cam = float(offsety_cam.get())
                z_cam = float(offsetz_cam.get())
                p_x1 = float(offsetx_pivot1.get())
                p_y1 = float(offsety_pivot1.get())
                p_z1 = float(offsetz_pivot1.get())
                p_x2 = float(offsetx_pivot2.get())
                p_y2 = float(offsety_pivot2.get())
                p_z2 = float(offsetz_pivot2.get())
                init_x = float(base_init_x.get())
                init_y = float(base_init_y.get())
                init_z = float(base_init_z.get())
                ppk_x = float(base_ppk_x.get())
                ppk_y = float(base_ppk_y.get())
                ppk_z = float(base_ppk_z.get())
                try:
                    epsg = int(type_epsg.get())
                    latence_value = int(latence.get())

                    data = read_data(fichierlog)
                    # gps = get_filtered_data(data,gps_value.get())
                    # offset_x, offset_y = dist_metric_to_wgs84(init_x-ppk_x , init_y-ppk_y,type_epsg.get())

                    offset_x = init_x-ppk_x
                    offset_y = init_y-ppk_y
                    offset_z = init_z-ppk_z
                    # offset = offset_x, offset_y, offset_z
                    # print(offset_x,offset_y)

                    #Quand le paramètre gps1 est gps
                    # if gps_value.get() == "GPS":
                    #     print("GPS 1")
                    #     x_gps = 0
                    #     y_gps = 0
                    #     z_gps = 0
                    structured_gps = get_structured_gps(data,gps_value.get(), latence_value)




                    structured_att = get_structured_data(data,"ATT")
                    cam = get_filtered_data(data,"CAM")
                    lat_interpolated , long_interpolated , alt_interpolated = tri_interpolate(structured_gps,7,8,9)
                    roll_interpolated , pitch_interpolated , yaw_interpolated = tri_interpolate(structured_att,3,5,7)

                    lat_interpolated = [row-offset_x for row in lat_interpolated]
                    long_interpolated = [row-offset_y for row in long_interpolated]
                    alt_interpolated = [row-offset_z for row in alt_interpolated]
                    # lat_interpolated , long_interpolated , alt_interpolated = lat_interpolated-offset_x , long_interpolated-offset_y, alt_interpolated-offset_z

                    # for a,b,c,d,e,f in zip(lat_interpolated , long_interpolated , alt_interpolated, roll_interpolated , pitch_interpolated , yaw_interpolated):
                    #     print(a,b,c,d,e,f)
                    time_US = [row[1] for row in cam]
                    srt = str(fichierlog.split('/')[-1]).split('.')[0]
                    
                    lat_interpolated_metric = list()
                    long_interpolated_metric = list()
                    for i in range(len(cam)):
                        lat_interpolated_metric.append(wgs84_to_metric(lat_interpolated[i],long_interpolated[i],type_epsg.get())[0])
                        long_interpolated_metric.append(wgs84_to_metric(lat_interpolated[i],long_interpolated[i],type_epsg.get())[1])

                    # for a,b,c,d,e,f in zip(lat_interpolated_metric , long_interpolated_metric , alt_interpolated, roll_interpolated , pitch_interpolated , yaw_interpolated):
                    #     print(a,b,c,d,e,f)

                    alt_interpolated_metric = alt_interpolated
                    
                    dx = list()
                    dy = list()
                    dz = list()
                    x_after_project_cam_in_gps = list()
                    y_after_project_cam_in_gps = list()
                    z_after_project_cam_in_gps = list()

                    angles = []
                    if(int(offset_pivot.get())):
                        
                        output_folder = custom_path+"/"+srt+" (pivot activé)"
                        path_detailed = output_folder+"/Récapitulatifs"
                        try:
                            mkdir(output_folder)
                        except OSError:
                            pass
                        try:
                            mkdir(path_detailed)
                        except OSError:
                            pass
                        
                        print(int(nacelle_fixe_boolean.get()))
                        
                        if int(nacelle_fixe_boolean.get())==0:
                            for line in data:
                                for elem in line:
                                    if elem == " MNT_RC_IN_TILT" :
                                        MNT_RC_IN_TILT = int(line[line.index(elem)+1])
                                        break

                            index_of_rcin = MNT_RC_IN_TILT+1
                            structured_rcin = get_structured_data(data, "RCIN")
                            rcin = interpolate(structured_rcin, index_of_rcin)
                            angles = [transform_to_angle(row) for row in rcin]


                        else:

                            try:
                                print(valeur_angle_fixe.get())
                                angle = int(valeur_angle_fixe.get())
                                for i in range(len(cam)):
                                    angles.append(angle)
                            except ValueError as e:
                                print(e)
                                error_type = 'VALEUR ANGLE INCORRECTE'
                                error_message = 'Entrer une valeur entière'
                                show_error()
                        print(angles)

                        for i in range(len(cam)):
                            new_x , new_y , new_z = project_cam_in_gps(lat_interpolated_metric[i], long_interpolated_metric[i], alt_interpolated[i],
                                                                roll_interpolated[i], pitch_interpolated[i], yaw_interpolated[i],
                                                                x_gps, y_gps,z_gps,
                                                                x_cam, y_cam , z_cam)
                            # print(new_x, new_y, new_z)
                            x , y , z = transform_with_pivots(new_x, new_y, new_z,
                                                            roll_interpolated[i], pitch_interpolated[i],yaw_interpolated[i],
                                                            p_x1, p_y1, p_z1,
                                                            p_x2, p_y2, p_z2,
                                                            angles[i])
                            x_after_project_cam_in_gps.append(x)
                            y_after_project_cam_in_gps.append(y)
                            z_after_project_cam_in_gps.append(z)
                            dx.append(lat_interpolated_metric[i] - x)
                            dy.append(long_interpolated_metric[i] - y)
                            dz.append(alt_interpolated[i] - z)
                        



                    else:
                        
                        output_folder = custom_path+"/"+srt+" (pivot désactivé)"
                        path_detailed = output_folder+"/Récapitulatifs"
                        try:
                            mkdir(output_folder)
                        except OSError:
                            pass
                        try:
                            mkdir(path_detailed)
                        except OSError:
                            pass

                        for i in range(len(cam)):
                            x , y , z = project_cam_in_gps(lat_interpolated_metric[i], long_interpolated_metric[i], alt_interpolated[i],
                                                            roll_interpolated[i], pitch_interpolated[i], yaw_interpolated[i],
                                                            x_gps, y_gps,z_gps,
                                                            x_cam, y_cam, z_cam)
                            x_after_project_cam_in_gps.append(x)
                            y_after_project_cam_in_gps.append(y)
                            z_after_project_cam_in_gps.append(z)
                            dx.append(lat_interpolated_metric[i] - x)
                            dy.append(long_interpolated_metric[i] - y)
                            dz.append(alt_interpolated[i] - z)

                    write_to_metric(prefix.get(),chiffre_depart.get(),suffix.get(), path_detailed,"position wgs84 interpolé.log",time_US,lat_interpolated, long_interpolated,alt_interpolated,roll_interpolated,pitch_interpolated,yaw_interpolated)
                    write_to_metric(prefix.get(),chiffre_depart.get(),suffix.get(), path_detailed,"position metric interpolé.log",time_US,lat_interpolated_metric, long_interpolated_metric,alt_interpolated_metric,roll_interpolated,pitch_interpolated,yaw_interpolated)
                    
                    indice_de_precision = []
                    for i, e in enumerate(cam):
                        # x_after_project_cam_in_gps[i] -= offset_x 
                        # y_after_project_cam_in_gps[i] -= offset_y
                        # z_after_project_cam_in_gps[i] -= offset_z
                        
                        statut_gps_avant = int(structured_gps[i][0][2])
                        statut_gps_apres = int(structured_gps[i][2][2])

                        if statut_gps_avant==6 and statut_gps_apres==6:
                            indice_de_precision.append(0.01)
                        elif statut_gps_apres==5 or statut_gps_apres ==5:
                            indice_de_precision.append(1)
                        elif statut_gps_avant<5 or statut_gps_apres<5 :
                            indice_de_precision.append(10)

                    write_csv(prefix.get(),
                                chiffre_depart.get(),
                                suffix.get(),
                                output_folder,
                                srt+"_geotag_metric.csv",
                                time_US,
                                x_after_project_cam_in_gps,
                                 y_after_project_cam_in_gps,
                                 z_after_project_cam_in_gps,
                                 roll_interpolated,
                                 pitch_interpolated,
                                 yaw_interpolated,
                                 indice_de_precision,
                                 angles)
                    write_log(prefix.get(),
                                chiffre_depart.get(),
                                suffix.get(),
                                output_folder,
                                srt+"_geotag_metric.log",
                                time_US,
                                x_after_project_cam_in_gps,
                                 y_after_project_cam_in_gps,
                                 z_after_project_cam_in_gps,
                                 roll_interpolated,
                                 pitch_interpolated,
                                 yaw_interpolated,
                                 indice_de_precision,
                                 angles)

                    lat_wgs_final = list()
                    long_wgs_final = list()
                    for i in range(len(cam)):
                        
                        lat_wgs_final.append(metric_to_wgs84(x_after_project_cam_in_gps[i],
                        y_after_project_cam_in_gps[i],
                        type_epsg.get())[0])
                        long_wgs_final.append(metric_to_wgs84(x_after_project_cam_in_gps[i],
                        y_after_project_cam_in_gps[i],
                        type_epsg.get())[1])
                   
                    alt_wgs_final = z_after_project_cam_in_gps

                    write_csv(prefix.get(),
                    chiffre_depart.get(),
                    suffix.get(),
                    output_folder,
                    srt+"_geotag_wgs84.csv",
                    time_US,
                    lat_wgs_final,
                    long_wgs_final,
                    alt_wgs_final,
                    roll_interpolated,
                    pitch_interpolated,
                    yaw_interpolated,
                    indice_de_precision,
                    angles)

                    write_log(prefix.get(),
                    chiffre_depart.get(),
                    suffix.get(),
                    output_folder,
                    srt+"_geotag_wgs84.log",
                    time_US,
                    lat_wgs_final,
                    long_wgs_final,
                    alt_wgs_final,
                    roll_interpolated,
                    pitch_interpolated,
                    yaw_interpolated,
                    indice_de_precision,
                    angles)


                    write_difference_log(prefix.get(),
                    chiffre_depart.get(),
                    suffix.get(),
                    path_detailed,
                    "différence(positionGPS-positionCAM).log",
                    time_US ,
                    dx ,
                    dy,
                    dz)

                    write_difference_csv(prefix.get(),
                    chiffre_depart.get(),
                    suffix.get(),
                    path_detailed,
                    "différence(positionGPS-positionCAM).csv",
                    time_US ,
                    dx ,
                    dy,
                    dz)


                    numero = list(np.arange(1,len(time_US)+1, 1))
                    labels_in_x = list(np.arange(0,len(time_US)+1,5))
                    dx_figure= plt.figure()
                    plt.title('dx en fonction du numéro photo')
                    plt.xlabel('Numéro photo')
                    plt.xticks(labels_in_x, fontsize=7)
                    plt.ylabel('positionGPS x en mètre - positionCAM x en mètre')
                    plt.grid(b = True)
                    # plt.plot(range(len(time_US)+1)[len(time_US):],dx,linestyle = "none" ,color = "black",markersize=1, marker ="o" , label = "dx en fonction du numéro photo")
                    plt.plot(numero,dx,linestyle = "none" ,color = "black",markersize=1, marker ="o" , label = "dx en fonction du numéro photo")
                    plt.legend(loc='upper right')
                    dx_figure.savefig(path_detailed+'/dx en fonction du numéro photo.png')

                    dy_figure= plt.figure()
                    plt.title('dy en fonction du numéro photo')
                    plt.xlabel('Numéro photo')
                    plt.xticks(labels_in_x, fontsize=7)
                    plt.grid(b = True)
                    plt.ylabel('positionGPS y en mètre - positionCAM y en mètre')
                    # plt.plot(range(len(time_US)+1)[len(time_US)-1:],dy,linestyle = "none" ,color = "black",markersize=1, marker ="o" ,label = "dy en fonction du numéro photo") 
                    plt.plot(numero,dy,linestyle = "none" ,color = "black",markersize=1, marker ="o" ,label = "dy en fonction du numéro photo") 
                    plt.legend(loc='upper right')
                    dy_figure.savefig(path_detailed+'/dy en fonction du numéro photo.png')

                    dz_figure= plt.figure()
                    plt.title('dz en fonction du numéro photo')
                    plt.xlabel('Numéro photo')
                    plt.xticks(labels_in_x, fontsize=7)
                    plt.grid(b = True)
                    plt.ylabel('positionGPS z en mètre - positionCAM z en mètre')
                    # plt.plot(range(len(time_US)+1)[len(time_US)-1:],dz,linestyle = "none" ,color = "black",markersize=1, marker ="o",label = "z en fonction du numéro photo")
                    plt.plot(numero,dz,linestyle = "none" ,color = "black",markersize=1, marker ="o",label = "z en fonction du numéro photo")
                    plt.legend(loc='upper right')
                    dz_figure.savefig(path_detailed+'/dz en fonction du numéro photo.png')

                    srt = str(fichierlog.split('/')[-1]).split('.')[0]
                    message = str('Verifier les résultats dans le dossier : \n'+custom_path+'/'+srt)
                    type_message = 'GEOTAGAGE TERMINE'

                    show_info()
                    output_folder= '\\'.join(output_folder.split('/'))
                    subprocess.call("explorer "+output_folder, shell=True)
                    
                except ValueError:
                    error_type = 'PARAMETRE EPSG INCORRECTE'
                    error_message = 'Entrer une valeur entière'
                    show_error()
                # except IndexError:
                #     error_type = 'FICHIER .LOG ou Paramètre GPS INCORRECTE '
                #     error_message = 'Sélectionner un fichier .log du drone correcte ou vérifier le paramètre GPS'
                #     show_error()
                except RuntimeError:
                    error_type = 'VALEUR EPSG INCORRECTE'
                    error_message = 'Voir www.spatialreference.com'
                    show_error()
                except PermissionError:
                    error_type = 'ACCES FICHIER IMPOSSIBLE'
                    error_message = 'Fermer tous les processus ouvrant vos fichiers'
                    show_error()
                except GpsException:
                    error_type = 'PARAMETRE GPS INCOMPATIBLE'
                    error_message = 'Le fichier log ne peut pas être traité par ce paramètre gps'
                    show_error()


            except ValueError:
               error_type = 'PARAMETRE OFFSET INCORRECTE'
               error_message = 'Entrer une valeur décimale'
               show_error()


    root = Tk()
    root.geometry("1200x800+150+0")
    root.minsize(1200,720)
    root.maxsize(1200,720)
    root.title('GEOTAG_DRONE')
    #titre fotsiny
    root.iconbitmap(resource_path('geotag_drone.ico'))
    image1 = Image.open(resource_path("image.png"))
    photo1 = ImageTk.PhotoImage(image1)
    image2 = Image.open(resource_path("inovadrone.png"))
    photo2 = ImageTk.PhotoImage(image2)

    cv = Canvas(root,width=1200,height=720)
    cv.pack(side='top', fill='both', expand='yes')
    cv.create_image(0, 0, image=photo1, anchor='nw')
    cv.create_image(30, 20, image=photo2, anchor='nw')

    font = Font(family='Century Gothique', size=45)
    cv.create_text(430,85,anchor='nw',fill='white',justify=CENTER,font=font,text='Geotag Drone')
    #boutton
    font_file = Font(family='Liberation Serif', size=12)
    titre_file = Label(root,text='Selectionner votre fichier log',font=font_file,anchor='w')
    titre_file.config(height='1', width='40')
    titre_file.place(relx=.04, rely=.27,anchor='w')

    titre_folder = Label(root,text='Selectionner votre dossier destination',font=font_file,anchor='w')
    titre_folder.config(height='1', width='40')
    titre_folder.place(relx=.5, rely=.27,anchor='w')

    filelog = StringVar(root,value='Aucun fichier choisi')
    open_file = Button(root,text="PARCOURIR", bg="#fe8134x", fg="white",command=OpenFile,highlightcolor="#fe8134x",activebackground="#fe8134x",activeforeground ="#fff")
    open_file.config(height='2',width='12')
    open_file.place(relx=.04, rely=.33, anchor="w")

    label_file = Label(root,textvariable=filelog,justify=LEFT,font=Font(family='Times New Roman', size=12),anchor='w')
    label_file.config(height=2, width=44)
    label_file.place(relx=.125, rely=.33,anchor='w')

    cv2 = Canvas(root,width=423,height=2,bg='#fe8134x')
    cv2.place(relx=0.125,rely=.355, anchor='w')

    folder_path = StringVar(root,value='Aucun dossier choisi')

    open_folder = Button(root,text="BROWSE OUTPUT", bg="#fe8134x", fg="white",command=browse_button,highlightcolor="#fe8134x",activebackground="#fe8134x",activeforeground ="#fff")
    open_folder.config(height='2',width='16')
    open_folder.place(relx=.5, rely=.33, anchor="w")

    label_folder = Label(root,textvariable=folder_path,justify=LEFT,font=Font(family='Times New Roman', size=12),anchor='w')
    label_folder.config(height=2, width=44)
    label_folder.place(relx=.607, rely=.33,anchor='w')

    cv2b = Canvas(root,width=395,height=2,bg='#fe8134x')
    cv2b.place(relx=0.607,rely=.355, anchor='w')

    cv3 = Canvas(root,width=250,height=50,bg='#ccc')
    cv3.place(relx=.04,rely=.42, anchor='w')
    cv3.create_text(50,25,anchor='w',fill='#000',justify=CENTER,font=Font(family='Liberation Serif', size=11),text='PARAMETRES GPS')

    gps_value = StringVar(root,value='GPS2')

    gps1 = Radiobutton(root, text="GPS 1 ", value="GPS", variable=gps_value, indicatoron=0, borderwidth=0, width=15, padx=1, pady=1, fg="#000", bg="#ccc", selectcolor="#fe8134x", activebackground="#fe8134x")
    gps1.place(relx=0.04, rely=.48)
    gps2 = Radiobutton(root, text="GPS 2 ",state='active', value="GPS2",variable = gps_value, indicatoron=0, borderwidth=0, width=15, padx=1, pady=1, fg="#000", bg="#ccc", selectcolor="#fe8134x", activebackground="#fe8134x")
    gps2.place(relx=0.155,rely=0.48)

    #VAOVAO
    cvo = Canvas(root,width=250,height=50,bg='#ccc')
    cvo.place(relx=.27,rely=.42, anchor='w')
    cvo.create_text(50,25,anchor='w',fill='#000',justify=CENTER,font=Font(family='Liberation Serif', size=11),text='PARAMETRE PIVOT')
    offset_pivot = StringVar(root,value=False)
    nacelle_fixe_boolean = StringVar(root,value=False)
    offset1 = Radiobutton(root, text="Activer ",command=activation_pivot,value=True, variable=offset_pivot, indicatoron=0, borderwidth=0, width=15, padx=1, pady=1, fg="#000", bg="#ccc", selectcolor="#fe8134x", activebackground="#fe8134x")
    offset1.place(relx=0.27, rely=.48)
    offset2 = Radiobutton(root, text="Desactiver",command=desactivation_pivot,state='active', value=False,variable = offset_pivot, indicatoron=0, borderwidth=0, width=15, padx=1, pady=1, fg="#000", bg="#ccc", selectcolor="#fe8134x", activebackground="#fe8134x")
    offset2.place(relx=0.385,rely=0.48)

    #fIN

    cv4 = Canvas(root,width=250,height=50,bg='#ccc')
    cv4.place(relx=.5,rely=.42, anchor='w')
    cv4.create_text(8,25,anchor='w',fill='#000',justify=CENTER,font=Font(family='Liberation Serif', size=11),text='CODE EPSG (spatialreference.org)')

    epsg_value = 23031
    type_epsg = Entry(root,bd=0,insertwidth=1,width=28,font = Font(family='Liberation Serif', size=12),textvariable=IntVar(root,value=23031),takefocus=0)
    type_epsg.place( relx=0.5,rely=0.48)

    #Latence
    cv42 = Canvas(root,width=250,height=50,bg='#ccc')
    cv42.place(relx=.73
    ,rely=.42, anchor='w')
    cv42.create_text(81,25,anchor='w',fill='#000',justify=CENTER,font=Font(family='Liberation Serif', size=11),text='LATENCE (ms)')

    latence = Entry(root,bd=0,insertwidth=1,width=28,font = Font(family='Liberation Serif', size=12),textvariable=IntVar(root,value=190),takefocus=0)
    latence.place( relx=0.73,rely=0.48)


    cv0 = Canvas(root,width=1080,height=2,bg='#fe8134x')
    cv0.place(relx=0.04,rely=.53, anchor='w')

    offsetx = IntVar(root,value=0)
    offsety = IntVar(root,value=0)
    offsetz = IntVar(root,value=0)

    cv5 = Canvas(root,width=300,height=50)
    cv5.place(relx=.04,rely=.569, anchor='w')
    cv5.create_text(80,25,anchor='w',fill='#E91E63',justify=CENTER,font=Font(family='Liberation Serif', size=12),text='OFFSET X (m)')

    """cv5a = Canvas(root,width=357,height=50,bg='#ccc')
    cv5a.place(relx=.04,rely=.825, anchor='w')
    cv5a.create_text(100,25,anchor='w',fill='#E91E63',justify=CENTER,font=Font(family='Liberation Serif', size=12),textvariable=offsetx)"""
    
    label_base_init = Label(root,text='base init', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_base_init.place(relx=0.04,rely=.567)
    base_init_x = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value= 0.0 ),takefocus=0)
    base_init_x.place(relx=.04,rely=.605, anchor='w')

    label_base_ppk = Label(root,text='base ppk', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_base_ppk.place(relx=0.04,rely=.62)
    base_ppk_x = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value= 0.0 ),takefocus=0)
    base_ppk_x.place(relx=.04,rely=.657, anchor='w')

    label_gps = Label(root,text='gps', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_gps.place(relx=0.04,rely=.67)
    offsetx_gps = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value= 0.0 ),takefocus=0)
    offsetx_gps.place(relx=.04,rely=.705, anchor='w')
    label_cam = Label(root,text='camera', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_cam.place(relx=0.04,rely=.72)
    offsetx_cam = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=0.18),takefocus=0)
    offsetx_cam.place(relx=.04,rely=.755, anchor='w')
    #offset pivot # x
    labelx_pivot1 = Label(root,text='pivot 1', font=Font(family='Liberation Serif', size=8),fg='#000')
    labelx_pivot1.place(relx=0.04,rely=.769)
    offsetx_pivot1 = Entry(root,bd=0,insertwidth=1,width=30,state='disable',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=0.105),takefocus=0)
    offsetx_pivot1.place(relx=.04,rely=.805, anchor='w')
    labelx_pivot2 = Label(root,text='pivot 2', font=Font(family='Liberation Serif', size=8),fg='#000')
    labelx_pivot2.place(relx=0.04,rely=.818)
    offsetx_pivot2 = Entry(root,bd=0,insertwidth=1,width=30,state='disable',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=-0.01),takefocus=0)
    offsetx_pivot2.place(relx=.04,rely=.855, anchor='w')

    cv6 = Canvas(root,width=300,height=50)
    cv6.place(relx=.38,rely=.569, anchor='w')
    cv6.create_text(80,25,anchor='w',fill='#E91E63',justify=CENTER,font=Font(family='Liberation Serif', size=12),text='OFFSET Y (m)')

    """cv6a = Canvas(root,width=357,height=50,bg='#ccc')
    cv6a.place(relx=.34,rely=.825, anchor='w')
    cv6a.create_text(110,25,anchor='w',fill='#E91E63',justify=CENTER,font=Font(family='Liberation Serif', size=12),textvariable=offsety)"""
    #offset pivot y
    label_base_init = Label(root,text='base init', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_base_init.place(relx=0.38,rely=.567)
    base_init_y = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value= 0.0 ),takefocus=0)
    base_init_y.place(relx=.38,rely=.605, anchor='w')

    label_base_ppk = Label(root,text='base ppk', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_base_ppk.place(relx=0.38,rely=.62)
    base_ppk_y = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value= 0.0 ),takefocus=0)
    base_ppk_y.place(relx=.38,rely=.657, anchor='w')

    label_gps = Label(root,text='gps', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_gps.place(relx=0.38,rely=.67)
    offsety_gps = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=0.0),takefocus=0)
    offsety_gps.place(relx=.38,rely=.705, anchor='w')
    label_cam = Label(root,text='camera', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_cam.place(relx=0.38,rely=.72)
    offsety_cam = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=0.0),takefocus=0)
    offsety_cam.place(relx=.38,rely=.755, anchor='w')

    
    labely_pivot1 = Label(root,text='pivot 1', font=Font(family='Liberation Serif', size=8),fg='#000')
    labely_pivot1.place(relx=0.38,rely=.769)
    offsety_pivot1 = Entry(root,bd=0,insertwidth=1,width=30,state='disable',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=0.11),takefocus=0)
    offsety_pivot1.place(relx=.38,rely=.805, anchor='w')
    labely_pivot2 = Label(root,text='pivot 2', font=Font(family='Liberation Serif', size=8),fg='#000')
    labely_pivot2.place(relx=0.38,rely=.818)
    offsety_pivot2 = Entry(root,bd=0,insertwidth=1,width=30,state='disable',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=-0.12),takefocus=0)
    offsety_pivot2.place(relx=.38,rely=.855, anchor='w')

    cv7 = Canvas(root,width=300,height=50)
    cv7.place(relx=.715,rely=.569, anchor='w')
    cv7.create_text(80,25,anchor='w',fill='#E91E63',justify=CENTER,font=Font(family='Liberation Serif', size=12),text='OFFSET Z (m)')

    """cv7a = Canvas(root,width=357,height=50,bg='#ccc')
    cv7a.place(relx=.64,rely=.825, anchor='w')
    cv7a.create_text(150,25,anchor='w',fill='#E91E63',justify=CENTER,font=Font(family='Liberation Serif', size=12),text='0',textvariable=offsetz)"""
    #offset pivot z

    label_base_init = Label(root,text='base init', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_base_init.place(relx=0.715,rely=.567)
    base_init_z = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value= 0.0 ),takefocus=0)
    base_init_z.place(relx=.715,rely=.605, anchor='w')

    label_base_ppk = Label(root,text='base ppk', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_base_ppk.place(relx=0.715,rely=.62)
    base_ppk_z = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value= 0.0 ),takefocus=0)
    base_ppk_z.place(relx=.715,rely=.657, anchor='w')

    label_gps = Label(root,text='gps', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_gps.place(relx=0.715,rely=.67)
    offsetz_gps = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=0.2),takefocus=0)
    offsetz_gps.place(relx=.715,rely=.705, anchor='w')
    label_cam = Label(root,text='camera', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_cam.place(relx=0.715,rely=.72)
    offsetz_cam = Entry(root,bd=0,insertwidth=1,width=30,font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=-0.44),takefocus=0)
    offsetz_cam.place(relx=.715,rely=.755, anchor='w')

    label_pivot1 = Label(root,text='pivot 1', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_pivot1.place(relx=0.715,rely=.769)
    offsetz_pivot1 = Entry(root,bd=0,insertwidth=1,width=30,state='disable',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=-0.025),takefocus=0)
    offsetz_pivot1.place(relx=.715,rely=.805, anchor='w')
    label_pivot2 = Label(root,text='pivot 2', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_pivot2.place(relx=0.715,rely=.818)
    offsetz_pivot2 = Entry(root,bd=0,insertwidth=1,width=30,state='disable',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=0),takefocus=0)
    offsetz_pivot2.place(relx=.715,rely=.855, anchor='w')


    process = Button(root,text="PROCESS", bg="#fe8134x", fg="white",command=process_button,font=Font(family='Liberation Serif', size=14),activebackground="#fe8134x",activeforeground ="#fff",highlightthickness=0,highlightbackground='#fff')
    process.config(height='2',width='20')
    process.place(relx=.40, rely=.95, anchor="w")
    help = Button(root,text="?", bg="#fe8134x", fg="white",command=help_button,font=Font(family='Liberation Serif', size=14),activebackground="#fe8134x",activeforeground ="#fff",highlightthickness=0,highlightbackground='#fff')
    help.place(relx=.97, rely=.95, anchor="w")


    # Interface de gestion resultat final
    cv1 = Canvas(root,width=270,height=2,bg='#fe8134x')
    cv1.place(relx=0.04,rely=.89, anchor='w')

    label_prefix = Label(root,text='Préfixe', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_prefix.place(relx=0.048,rely=.920)
    prefix = Entry(root,bd=0,insertwidth=1,width=6,state='normal',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value="_DSC0"),takefocus=0)
    prefix.place(relx=0.04,rely=.960, anchor='w')

    label_chiffre_depart = Label(root,text='Chiffre de départ', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_chiffre_depart.place(relx=0.117,rely=.920)
    chiffre_depart = Entry(root,bd=0,insertwidth=1,width=10,state='normal',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=1),takefocus=0)
    chiffre_depart.place(relx=0.117,rely=.960, anchor='w')
    
    label_suffix = Label(root,text='Suffixe', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_suffix.place(relx=0.225,rely=.920)
    suffix = Entry(root,bd=0,insertwidth=1,width=6,state='normal',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=".JPG"),takefocus=0)
    suffix.place(relx=0.22,rely=.960, anchor='w')

    # Interface configuration nacelle
    cv2 = Canvas(root,width=270,height=2,bg='#fe8134x')
    cv2.place(relx=0.715,rely=.89, anchor='w')
    nacelle_fixe_radio = Radiobutton(root, text="Nacelle Fixe",command=nacelle_fixe,value=True, variable=nacelle_fixe_boolean, indicatoron=0, borderwidth=0, width=16, padx=1, pady=1, fg="#000", bg="#ccc", selectcolor="#fe8134x", activebackground="#fe8134x")
    nacelle_fixe_radio.place(relx=0.7155, rely=.91)
    nacelle_mobile_radio = Radiobutton(root, text="Nacelle Mobile",command=nacelle_mobile,state='active', value=False,variable = nacelle_fixe_boolean, indicatoron=0, borderwidth=0, width=16, padx=1, pady=1, fg="#000", bg="#ccc", selectcolor="#fe8134x", activebackground="#fe8134x")
    nacelle_mobile_radio.place(relx=0.845,rely=0.91)

    label_valeur_angle_fixe = Label(root,text='Angle en degré', font=Font(family='Liberation Serif', size=8),fg='#000')
    label_valeur_angle_fixe.place(relx=0.715,rely=.95)
    valeur_angle_fixe = Entry(root,bd=0,insertwidth=1,width=3,state='disable',font = Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value="-90"),takefocus=0)
    valeur_angle_fixe.place(relx=0.79,rely=.960, anchor='w')

    root.mainloop()