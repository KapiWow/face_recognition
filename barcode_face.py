#!/home/kapi/anaconda3/bin/python3

import PySimpleGUI as sg
import os
import io
import barcode
import png
from barcode.writer import ImageWriter

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import random
from numpy import linalg as LA
from scipy.fftpack import dct
import matplotlib.pyplot as plt
from skimage.transform import rescale, resize, downscale_local_mean



from PIL import Image

def get_img_data(f, maxsize=(1200, 850)):
    """
    Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

cwd = os.getcwd()

bins = [
        [15, 25, 40, 51, 65, 87, 119, 172, 312], 
        [111, 207, 347, 454, 643, 808, 987, 1193, 1447], 
        [371, 506, 593, 732, 860, 1001, 1193, 1408, 1698], 
        [412, 519, 616, 695, 776, 865, 1020, 1137, 1301], 
        [436, 537, 631, 747, 847, 941, 1063, 1243, 1515], 
        [515, 691, 798, 888, 1014, 1101, 1232, 1470, 1734], 
        [633, 795, 929, 1052, 1190, 1316, 1407, 1523, 1684], 
        [710, 801, 897, 1010, 1098, 1181, 1300, 1443, 1679], 
        [632, 747, 814, 888, 944, 996, 1075, 1227, 1487], 
        [400, 621, 716, 788, 835, 906, 992, 1089, 1237], 
        [94, 281, 548, 690, 787, 840, 914, 1026, 1219], 
        [30, 51, 93, 251, 517, 714, 822, 910, 1101], 
        [6, 11, 15, 23, 41, 124, 338, 699, 939]
]

def hist(img, count):
    res, _ = np.histogram(img, bins=count)
    return res;

def get_picture(path):
    #address = "data/s" + str(0+1) + "/" + str(0+1) + ".pgm"
    pic = mpimg.imread(path)
    if (pic.shape != (112, 92)):
        return False, pic
    return True, pic


def scale(img, mult):
    res = rescale(img, mult, anti_aliasing=False) * 255
    return res.astype(np.uint8)


barcode_column = [
    [sg.Text('File 1'), sg.InputText(), sg.FileBrowse()],
    #[sg.Image(key='image', size=(5, 6))],
    [sg.Image(key='image', size=(5, 6))], 
    [sg.Submit("Ok"), sg.Cancel()]
]

image_column = [
    [sg.Image(key='pic', size=(5, 6))]
]


layout = [
    [
        sg.Column(barcode_column),
        sg.VSeperator(),
        sg.Column(image_column),
    ]
]

window = sg.Window('Barcode', layout)
while True:                             # The Event Loop
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break

    if event == 'Ok':
        path = values[0]
        #path = "/home/kapi/project/face_recognition/data/s1/1.pgm"
        if ".pgm" in path:
            img = np.array([])
            is_valid, img = get_picture(path)
            if is_valid:
                print(img)
                i_hist = hist(img,13)
                print(i_hist)
                
                res = ""
                for j in range(13):
                    val = i_hist[j]
                    if val <= bins[j][8]:
                        for k in range(9):
                            if val <= bins[j][k]:
                                res += str(k)
                                break
                                
                    else:
                        res += str(9)
                print(res)
                EAN = barcode.get_barcode_class('ean13')
                ean = EAN(res, writer=ImageWriter())
                fullname = ean.save('barcode')
                window.Element('image').Update(data=get_img_data(fullname))
                    
                img = scale(img, 3)
                #img_png = []
                #for i in img:
                #    col = []
                #    for j in i:
                #        col.append(j)
                #    img_png.append(col)
                #img_png = np.array(img_png)
                

                res_png = png.from_array(img, 'L').save("temp.png")
                window.Element('pic').Update(data=get_img_data("temp.png"))




