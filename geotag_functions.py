from csv import *
from numpy import array
from pyproj import Proj, transform
from math import cos,sin,pi,radians

class GpsException(Exception):
    pass

def read_data(filename) :
    c = []
    with open(filename, mode='r', encoding="utf-8") as f :
        csv = reader(f, delimiter=",")
        for line in csv :
            c.append(line)
    return c

def write_data(prefix,start,suffix,path,filename,timeUS,long_,lat,alt,roll,pitch,yaw):
    try:
        start = int(start)
    except ValueError:
        start = 0
    with open(path+'/'+filename,'w', newline="") as csvfile:
        spamwriter = writer(csvfile, delimiter =",",quotechar ='|')
        spamwriter.writerow(["CAM","TimeUS","Longitude","Latitude","Altitude","Roll","Pitch","Yaw"])
        for i in range(len(timeUS)):
            spamwriter.writerow([prefix+str(start+i)+suffix,timeUS[i],str(long_[i]),str(lat[i]),str(alt[i]),roll[i],pitch[i],yaw[i]])

def write_to_metric(prefix,start,suffix,path,filename,timeUS,lat,long_,alt,roll,pitch,yaw):
    try:
        start = int(start)
    except ValueError:
        start = 0
    with open(path+'/'+filename,'w', newline="") as csvfile:
        spamwriter = writer(csvfile, delimiter =",",quotechar ='|')
        spamwriter.writerow(["CAM","TimeUS","Xprov","Yprov","Zprov","Roll","Pitch","Yaw"])
        for i in range(len(timeUS)):
            spamwriter.writerow([prefix+str(start+i)+suffix,timeUS[i],lat[i],long_[i],alt[i],roll[i],pitch[i],yaw[i]])

def write_difference_log (prefix,start,suffix,path,filename,timeUS,diff_long , diff_lat, diff_alt):
    try:
        start = int(start)
    except ValueError:
        start = 0
    with open(path+'/'+filename,'w', newline="") as csvfile:
        spamwriter = writer(csvfile, delimiter =",",quotechar ='|')
        spamwriter.writerow(["CAM","dx","dy","dz"])
        for i in range(len(timeUS)):
            spamwriter.writerow([prefix+str(start+i)+suffix,diff_long[i],diff_lat[i], diff_alt[i]])

def write_difference_csv (prefix,start,suffix,path,filename,timeUS,diff_long , diff_lat, diff_alt):
    try:
        start = int(start)
    except ValueError:
        start = 0
    with open(path+'/'+filename,'w', newline="") as csvfile:
        spamwriter = writer(csvfile, delimiter =";",quotechar ='|')
        spamwriter.writerow(["CAM","dx","dy","dz"])
        for i in range(len(timeUS)):
            spamwriter.writerow([prefix+str(start+i)+suffix,diff_long[i],diff_lat[i], diff_alt[i]])

def write_csv (prefix,start,suffix,path,filename,timeUS, diff_lat , diff_long, diff_alt ,r, p, y,precision,angles):
    try:
        start = int(start)
    except ValueError:
        start = 0
    with open(path+'/'+filename,'w', newline="") as csvfile:
        spamwriter = writer(csvfile, delimiter =";",quotechar ='|')
        if len(angles) !=0:
            spamwriter.writerow(["CAM","TimeUS", "X","Y","Z","Roll","Pitch","Yaw","Indice de précision (cm)","Angle nacelle"])
            for i in range(len(timeUS)):
                spamwriter.writerow([prefix+str(start+i)+suffix,timeUS[i],str(diff_lat[i]),str(diff_long[i]), str(diff_alt[i]), r[i],p[i] ,y[i],precision[i],angles[i]])
        else:
            spamwriter.writerow(["CAM","TimeUS", "X","Y","Z","Roll","Pitch","Yaw","Indice de précision (cm)"])
            for i in range(len(timeUS)):
                spamwriter.writerow([prefix+str(start+i)+suffix,timeUS[i],str(diff_lat[i]),str(diff_long[i]), str(diff_alt[i]), r[i],p[i] ,y[i],precision[i]])

def write_log (prefix,start,suffix,path,filename, timeUS, diff_lat , diff_long, diff_alt ,r, p, y,precision,angles):
    try:
        start = int(start)
    except ValueError:
        start = 0
    with open(path+'/'+filename,'w', newline="") as csvfile:
        spamwriter = writer(csvfile, delimiter =",",quotechar ='|')
        if len(angles) !=0:
            spamwriter.writerow(["CAM","TimeUS", "X","Y","Z","Roll","Pitch","Yaw","Indice de précision (cm)","Angle nacelle"])
            for i in range(len(timeUS)):
                spamwriter.writerow([prefix+str(start+i)+suffix,timeUS[i],str(diff_lat[i]),str(diff_long[i]), str(diff_alt[i]), r[i],p[i] ,y[i],precision[i],angles[i]])
        else:
            spamwriter.writerow(["CAM","TimeUS", "X","Y","Z","Roll","Pitch","Yaw","Indice de précision (cm)"])
            for i in range(len(timeUS)):
                spamwriter.writerow([prefix+str(start+i)+suffix,timeUS[i],str(diff_lat[i]),str(diff_long[i]), str(diff_alt[i]), r[i],p[i] ,y[i],precision[i]])


def get_structured_gps(data,delimiter, latence):

    f = []
    for i,line in enumerate(data) :
        if line:
            if (line[0] == "CAM"):
                temp = []
                j=i-1+latence
                k=i+1+latence
                while data[j][0] != delimiter:
                    j-=1

                while data[k][0] != delimiter:
                    k+=1

                # if data[k][0] !=delimiter or data[j][0] !=delimiter:
                #     raise GpsException("Paramètre GPS Incompatible")
                temp.append(data[j])
                temp.append(line)
                temp.append(data[k])
                f.append(temp)
                # data[j][7] = str(float(data[j][7])+ offset[0])
                # data[j][8] = str(float(data[j][8])+ offset[1])
                # data[j][9] = str(float(data[j][9])+ offset[2])

                # data[k][7] = str(float(data[j][7])+ offset[0])
                # data[k][8] = str(float(data[j][8])+ offset[1])
                # data[k][9] = str(float(data[j][9])+ offset[2])
    # print(f)
    return f


def get_structured_data(data,delimiter):

    f = []
    for i,line in enumerate(data) :
        if line :
            if (line[0] == "CAM"):
                temp = []
                j=i-1
                k=i+1


                while data[j][0] != delimiter:
                    j-=1

                while data[k][0] != delimiter:
                    k+=1

                temp.append(data[j])
                temp.append(line)
                temp.append(data[k])
                f.append(temp)
    return f

def get_filtered_data(data,field):
    result = []
    for line in data:
        if line:
            if line[0]== field:
                result.append(line)
    return result

def interpolate(structured_data, field):
    """
    Interpolation linéaire sur les données les plus proches du structured_data
    """
    interp = []
    for element in structured_data :
        a = float(element[2][field])-float(element[0][field])
        delta21 = float(element[1][1])-float(element[0][1])
        delta31 = float(element[2][1])-float(element[0][1])
        temp = (a*delta21)/delta31+float(element[0][field])
        interp.append(temp)

    return interp
def tri_interpolate(structured_data, first_field , second_field, third_field):

    """
    Interpolation linéaire sur les données les plus proches du structured_data
    """

    first_interp = []
    second_interp = []
    third_interp = []

    for element in structured_data :
        a = float(element[2][first_field])-float(element[0][first_field])
        delta21 = float(element[1][1])-float(element[0][1])
        delta31 = float(element[2][1])-float(element[0][1])
        temp = (a*delta21)/delta31+float(element[0][first_field])
        first_interp.append(temp)

        a = float(element[2][second_field])-float(element[0][second_field])
        delta21 = float(element[1][1])-float(element[0][1])
        delta31 = float(element[2][1])-float(element[0][1])
        temp = (a*delta21)/delta31+float(element[0][second_field])
        second_interp.append(temp)

        a = float(element[2][third_field])-float(element[0][third_field])
        delta21 = float(element[1][1])-float(element[0][1])
        delta31 = float(element[2][1])-float(element[0][1])
        temp = (a*delta21)/delta31+float(element[0][third_field])
        third_interp.append(temp)

    return first_interp , second_interp , third_interp

def wgs84_to_metric(lat, long_, epsg):

    inProj = Proj(init='epsg:4326')#wgs84
    outProj = Proj(init='epsg:'+str(epsg))#UTM 31N

    return transform(inProj,outProj,long_,lat)

def metric_to_wgs84(lat, long_,epsg):

    outProj = Proj(init='epsg:4326')#wgs84
    inProj = Proj(init='epsg:'+str(epsg))#UTM 31N
    a, b = transform(inProj,outProj,lat,long_)
    return b, a

def dist_metric_to_wgs84(dist_lat, dist_long_,epsg):
    outproj = Proj(init='epsg:4326')#wgs84
    inproj = Proj(init='epsg:'+str(epsg))#UTM 31N

    x = transform(inproj, outproj,dist_lat ,dist_long_)[0] - transform(inproj, outproj,0 ,0)[0]
    y = transform(inproj, outproj,dist_lat ,dist_long_)[1] - transform(inproj, outproj,0 ,0)[1] 

    return x, y

def dist_wgs84_to_metric(dist_lat, dist_long_,epsg):
    inproj = Proj(init='epsg:4326')#wgs84
    outproj = Proj(init='epsg:'+str(epsg))#UTM 31N

    x = transform(outproj, inproj,dist_lat ,dist_long_)[0] - transform(outproj, inproj,0 ,0)[0]
    y = transform(outproj, inproj,dist_lat ,dist_long_)[1] - transform(outproj, inproj,0 ,0)[1] 

    return x, y

def project_cam_in_gps (lat ,_long ,alt, roll, pitch, yaw, gpsx, gpsy , gpsz, camx, camy, camz):

    #angle de rotation % a x
    w_x = radians(roll)
    #angle de rotation % a y
    w_y = radians(pitch)
    #angle de rotation % a z
    w_z = radians(-yaw)
    #calcul des trigonometrie des rotations
    cx = cos(w_x)
    cy = cos(w_y)
    cz = cos(w_z)

    sx = sin(w_x)
    sy = sin(w_y)
    sz = sin(w_z)

    #matrice de la transformation rotation et translationx
    M1 = array([[1,0,0],[0,cx,-sx],[0,sx,cx]])
    M2 = array([[cy,0,sy],[0,1,0],[-sy,0,cy]])
    M3 = array([[cz,-sz,0],[sz,cz,0],[0,0,1]])

    #offset camera

    # rotation au centre du drone   
    camx, camy, camz = M1.T.dot(array([camx, camy, camz])) 
    camx, camy, camz = M2.T.dot(array([camx, camy, camz]))
    camx, camy, camz = M3.T.dot(array([camx, camy, camz]))
    
    
    gpsx,gpsy,gpsz = M1.T.dot(array([gpsx,gpsy,gpsz]))
    gpsx,gpsy,gpsz = M2.T.dot(array([gpsx,gpsy,gpsz]))
    gpsx,gpsy,gpsz = M3.T.dot(array([gpsx,gpsy,gpsz]))


    newx , newy , newz = lat-gpsx+camx, _long-gpsy+camy , alt-gpsz+camz
    return newx, newy, newz

def transform_with_pivots (lat ,_long ,alt,
                                         roll, pitch,yaw,
                                         p2_x,p2_y,p2_z,
                                         p3_x,p3_y,p3_z,
                                         rcin):
    ym = lat
    xm = _long
    zm = alt
    #angle de rotation % a x
    w_x = radians(roll)
    #angle de rotation % a y
    w_y = radians(pitch)

    w_z = radians(-yaw)

    cx = cos(w_x)
    sx = sin(w_x)
    cz = cos(w_z)
    
    cy = cos(w_y)
    sy = sin(w_y)
    sz = sin(w_z)

    Rx = array([[1, 0, 0], [0, cx, -sx],[0, sx, cx]])
    Rz = array([[cz, -sz, 0], [sz, cz, 0],[0, 0, 1]])
    Ry = array([[cy, 0,sy], [0, 1, 0],[-sy, 0, cy]])

    pivot2_x,pivot2_y,pivot2_z =  Ry.T.dot(array([p2_x, p2_y, p2_z]))

    # print(pivot2_x,pivot2_y,pivot2_z)
    pivot3_x = p3_x*cos(radians(rcin))
    pivot3_z = p3_x*sin(radians(rcin))
    pivot3_y = p3_y

    x = pivot2_x+pivot3_x
    y = pivot2_y+pivot3_y
    z = pivot2_z+pivot3_z

    x,y,z = Rz.T.dot(array([x,y,z])) + array([lat, _long, alt])
    # print(x,y,z)
    return x,y,z

def transform_to_angle(rcin):
    return (rcin*18-27000)/100
