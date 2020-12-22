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
import copy
import qrcode


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


qr_column = [
    [sg.Text('num'), sg.InputText()],
    [sg.Submit("Ok"), sg.Cancel()],
    [sg.Image(key='qr', size=(5, 6))]
]

image_column = [
    [sg.Image(key='image', size=(5, 6))]
]

point_column = [
    [sg.Image(key='point', size=(5, 6))]
]


layout = [
    [
        sg.Column(qr_column),
        sg.VSeperator(),
        #sg.Column(image_column),
        #sg.VSeperator(),
        sg.Column(point_column),
    ]
]


def load_data(num):
    img = mpimg.imread("qr/300W/01_Indoor/indoor_"+num+".png")
    text = open("qr/300W/01_Indoor/indoor_"+num+".pts", "r").read()
    return img,text

def set_pixel(img,x,y,val):
    img[x][y][0] = val
    img[x][y][1] = val
    img[x][y][2] = val

def process_img(data, img):
#     mpimg.imsave(address, final)
    qr_data = "" 
    img_points = copy.deepcopy(img)
    for line in data.splitlines()[3:-2]:
    #     print(line)
        #qr_data += line[0:3] + line[8:11]
        num = line.find(" ")
        first = line[0:num]
        last = line[num:-1]

        x = int(float(last))
        y = int(float(first))
        qr_data += str(x) + str(y)
        set_pixel(img_points, x, y, 1)
        set_pixel(img_points, x+1, y+1, 1)
        set_pixel(img_points, x-1, y+1, 1)
        set_pixel(img_points, x-1, y-1, 1)
        set_pixel(img_points, x+1, y-1, 1)
    return qr_data, img_points



window = sg.Window('Barcode', layout)
while True:                             # The Event Loop
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break

    if event == 'Ok':
        num = values[0]
        
        img, data = load_data(num)
        qr_data, points = process_img(data,img)
        

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")


        count = 1
        img_res = copy.deepcopy((img*255).astype(int))
        img_save = np.asarray(qr_img)
        
        for i in range(len(img_save)):
            for j in range(len(img_save[i])):
                img_res[i][j][0] -= img_res[i][j][0]%(2**count)
                img_res[i][j][0] += int((2**count - 1)*img_save[i][j])
        img_res = img_res.astype(np.uint8) 
        mpimg.imsave("res.png", img_res)
        mpimg.imsave("qr/temp1.png", qr_img, cmap='gray')
        mpimg.imsave("qr/temp2.png", points)

        #res_png = png.from_array(img, 'L').save("temp.png")
        #window.Element('image').Update(data=get_img_data("res.png"))
        window.Element('point').Update(data=get_img_data("qr/temp2.png"))
        window.Element('qr').Update(data=get_img_data("qr/temp1.png"))




