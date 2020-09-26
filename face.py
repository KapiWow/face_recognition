# imports
%pylab inline
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import random
from numpy import linalg as LA

import matplotlib.pyplot as plt

def dist(img1, img2):
    res = 0
    for i in range(len(img1)):
        res += abs(int(img1[i]) - int(img2[i]))
    return res;

    #initialization
def load():
    class_count = 40
    image_count = 10
    imgs = []
    for i in range(class_count):
        imgs.append([])
        for j in range(image_count):
            address = "data/s" + str(i+1) + "/" + str(j+1) + ".pgm"
            imgs[i].append(mpimg.imread(address))
    return imgs

    #set test, train

def test_train(imgs, count):
    train = []
    test = []
    for i in imgs:
        train.append(i[:count])
        test.append(i[count:])
    return test, train

def scale(img, mult):
    res = []
    h = len(img)
    w = len(img[0])
    h_count = int(h/mult)
    w_count = int(w/mult)
    for i in range(h_count):
        for j in range (int(w_count)):
            res.append(0)
            value = 0
            for q in range(mult):
                for p in range(mult):
                    value += img[i*mult+q][j*mult+p];
            value = value / mult*mult;
            res.append(value)
    
    for i in range(w_count*h_count):
        res[i] = res[i]/mult/mult
        
    return res

def random_list(count,img):
    h = len(img)
    w = len(img[0])
    res = []
    for i in range(count):
        r = int(random.random()*(h*w-1))
        elem = []
        elem.append(int(r/w))
        elem.append(r%w)
        res.append(elem)
    return res

def random_img(img, rand_list):
    res = []
    for i in rand_list:
        res.append(img[i[0]][i[1]])
    return res

def fft(img, size):
    size2 = [5,5]
    res = []
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    for i in range(int(len(fshift)/2-size[0]), int(len(fshift)/2+size[0])):
        for j in range(int(len(fshift[0])/2-size[1]), int(len(fshift[0])/2+size[1])):
            res.append(fshift[i][j])
    return res;

def dist_complex(img1, img2):
    res = 0
    for i in range(len(img1)):
        res += abs(img1[i] - img2[i])
    return res;

def hist(img, count):
    res = []
    for i in range(count):
        res.append(0)
    for i in img:
        for j in i:
            res[int((j/255)*count)] += 1
    return res;

def grad(img, W, S):
    res = []
    for i in range(S,int((len(img)-W)/S)):
        value = 0
        for j in range(W*len(img[0])):
            id_h = int(i*S+j/(len(img[0])))
            id_w = int(j%(len(img[0])))
            value += abs(img[id_h][id_w] - img[id_h-S][id_w])
        res.append(value)
    return res

def vote(result, class_count):
    voted = []
    for i in range (len(result[0])):
        value = [0]*class_count
        for j in result:
            value[j[i]] += 1
        max_id = 0
        max_value = value[0]
        for i in range(len(value)):
            if (value[i] > value[max_id]):
                max_id = i
                max_value = value[i]
        voted.append(max_id)
    return voted

def fr(test, train):
    res = 0
    res_list = []
    for i in range(len(test)):
#         res_list.append([])
        for j in range(len(test[0])):
            i_id = 0
            image_m = test[i][j]
            i_dist_min = dist(image_m, train[0][0])
            for q in range(len(train)):
                for p in range(len(train[0])):
                    i_dist = dist(image_m, train[q][p])
                    if (i_dist < i_dist_min):
                        i_dist_min = i_dist
                        i_id = q
            if (i_id == i):
                res += 1
            res_list.append(i_id)
    print(res/(10-count_to_load)/40)
    return res_list
            
def fr_pic(test, train):
    res = 0
    res_list = []
    for i in range(len(test)):
#         res_list.append([])
        for j in range(len(test[0])):
            i_id = 0
            i_num = 0
            image_m = test[i][j]
            i_dist_min = dist(image_m, train[0][0])
            for q in range(len(train)):
                for p in range(len(train[0])):
                    i_dist = dist(image_m, train[q][p])
                    if (i_dist < i_dist_min):
                        i_dist_min = i_dist
                        i_num = p
                        i_id = q
            if (i_id == i):
                res += 1
            res_list.append([i_id, i_num])
#     print(res/(10-count_to_load)/40)
    return res_list


imgs = load()
count_to_load = 5
class_count = 40
test, train = test_train(imgs, count_to_load)
result = []
for i in range(10):
    result.append([])
    for j in range(5):
        result[i].append([])
        
# result = [[[]]*5]*9
print(result)

imgs_scaled = []
image_count = 10
class_count = 40
mult = 4
for i in range(class_count):
    imgs_scaled.append([])
    for j in range(image_count):
#         print(i,j)
        imgs_scaled[i].append(scale(imgs[i][j], mult))

imgs_random = []
image_count = 10
class_count = 40
count = 800
rand_list = random_list(count, imgs[0][0])
for i in range(class_count):
    imgs_random.append([])
    for j in range(image_count):
        imgs_random[i].append(random_img(imgs[i][j], rand_list))

imgs_fft = []
image_count = 10
class_count = 40
size = [5,5]
for i in range(class_count):
    imgs_fft.append([])
    for j in range(image_count):
        imgs_fft[i].append(fft(imgs[i][j], size))

imgs_hist = []
count = 32
for i in range(class_count):
    imgs_hist.append([])
    for j in range(image_count):
        imgs_hist[i].append(hist(imgs[i][j], count))


imgs_grad = []
W = 10
S = 2
for i in range(class_count):
    imgs_grad.append([])
    for j in range(image_count):
        imgs_grad[i].append(grad(imgs[i][j], W, S))


mult = 8
test_count = 10
for i in range(1,test_count):
    count_to_load = i
    class_count = 40
    test, train = test_train(imgs_scaled, count_to_load)
    result[i-1][0] = (fr(test, train))


for i in range(1,test_count):
    count_to_load = i
    class_count = 40
    test, train = test_train(imgs_random, count_to_load)
    result[i-1][1] = (fr(test, train))

for i in range(1,test_count):
    count_to_load = i
    class_count = 40
    test, train = test_train(imgs_fft, count_to_load)
    result[i-1][2] = (fr(test, train))

for i in range(1,test_count):
    count_to_load = i
    class_count = 40
    test, train = test_train(imgs_hist, count_to_load)
    result[i-1][3] = (fr(test, train))

for i in range(1,test_count):
    count_to_load = i
    class_count = 40
    test, train = test_train(imgs_grad, count_to_load)
    result[i-1][4] = (fr(test, train))

graph_data = [[]]
picture_data = [[],[],[],[],[],[]]

# res = result[0][0]
for c in range(1,test_count):
    res = result[c-1]
# print(res)
    voted = vote(res, class_count)
    right = []
    count_to_load = c
    for i in range(40):
        for j in range(10-count_to_load):
            right.append(i)
#     print(right)
    ans = 0
    t = voted
    res = 0
    for i in range(len(t)):
        if (t[i] == right[i]):
            ans += 1
    print(ans/len(t))
    graph_data[0].append(ans/len(t))
    if (c == 6):
        picture_data[0]=voted
#         print(1)
#     print(len(t))



for method_num in range(5):
    graph_data.append([])    
    for c in range(1,test_count):
        res = [result[c-1][method_num]]
# print(res)
        voted = vote(res, class_count)
        right = []
        count_to_load = c
        for i in range(40):
            for j in range(10-count_to_load):
                right.append(i)
#     print(right)
        ans = 0
        t = voted
        res = 0
        for i in range(len(t)):
            if (t[i] == right[i]):
                ans += 1
        print(method_num, c, ans/len(t))
        graph_data[method_num+1].append(ans/len(t))
        
        if (c == 6):
            picture_data[method_num+1]=voted


x = [1,2,3,4,5,6,7,8,9]
plt.title('Dependencies from count of etalons')   # заголовок
plt.xlabel('etalon count')   # подпись оси OX
plt.ylabel('accuracy')   # подпись оси OY
plt.plot(x,graph_data[0], label = "parallel", linewidth=10.0)
plt.plot(x,graph_data[1], label = "scale", linewidth=5.0)
plt.plot(x,graph_data[2], label = "random", linewidth=5.0)
plt.plot(x,graph_data[3], label = "fft", linewidth=5.0)
plt.plot(x,graph_data[4], label = "hist", linewidth=5.0)
plt.plot(x,graph_data[5], label = "grad", linewidth=5.0)

plt.legend()   # легенда


rcParams['figure.figsize'] = 6, 5
rcParams['figure.dpi'] = 80

picture_data = [[],[],[],[],[],[],[]]
for i in range(0,40):
    for j in range(7,11):
        picture_data[6].append(j)
count_to_load = 6
test, train = test_train(imgs_scaled, count_to_load)
picture_data[0] = (fr_pic(test, train))