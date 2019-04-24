# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 09:11:45 2019

@author: VietPhan
"""
import math
import cv2
import numpy as np
import time
start  = time.time()

def hist_equalizer(img):
	b,g,r = cv2.split(img)
	red = cv2.equalizeHist(r)
	green = cv2.equalizeHist(g)
	blue = cv2.equalizeHist(b)
    
	return cv2.merge((blue,green,red))
def colordist(x,v):
    x_square  = np.inner(x,x)
    v_square  = np.inner(v,v)
    xv_square = np.inner(x,v)*np.inner(x,v)
    p_square = (xv_square)/v_square
    return math.sqrt(abs(x_square-p_square))
def brightness(v,C):
    I = v[0] + v[1] + v[2]
    I_max = C[1][1]#C11 = I max
    I_min = C[1][0]#C10 = I min
    I_low = alpha*I_max
    I_hi = max(beta*I_max,I_min/alpha)
    if I<=I_hi and I>=I_low:
        return True
    return False
def find_match(x,C):
    for i in range(len(C)):
        #print(colordist(x,C[i][0]))
        if colordist(x,C[i][0]) <=eps1 and brightness(x,C[i]) == True:
           # print('match')
            Bm = x[0]
            Gm = x[1]
            Rm = x[2]
            B = C[i][0][0]
            G = C[i][0][1]
            R = C[i][0][2]
            I = Bm+Gm+Rm
            I_min = C[i][1][0]
            I_max = C[i][1][1]
            f = C[i][1][2]
            lamda = C[i][1][3]
            p = C[i][1][4]
            q = C[i][1][5]
            C[i][0] = [(f*Rm+R)/(f+1),(f*Gm+G)/(f+1),(f*Bm+B)/(f+1)]
            C[i][1] = [min(I,I_min),max(I,I_max),f+1,max(lamda,t-q),p,t]
            return True      
    return False
def find_match2(x,C):
    for i in range(len(C)):
        #print(colordist(x,C[i][0]))
        if colordist(x,C[i][0]) <=eps2 and brightness(x,C[i]) == True:
            return True      
    return False    
N = 5 #sample of background trainning
eps1 = 10  #trainning threshold
eps2 = 30 #detection threshold
alpha = 0.7
beta = 1.1

#cap = cv2.VideoCapture('test2.mp4')
#_,frame = cap.read()
frame = cv2.imread('1_2.JPEG')
#frame = hist_equalizer(frame)
H,W,channel = frame.shape

Map = [[[] for x in range (W)] for y in range (H)]
for i in range(N):
    #_,frame = cap.read()
    t = i+1
    I = 0
    print(i)
    for h in range(H):
        for w in range(W):
            B = float(frame[h,w,0])
            G = float(frame[h,w,1])
            R = float(frame[h,w,2])
            x = [B,G,R]
            I = B+G+R
            if Map[h][w] == None or find_match(x,Map[h][w]) == False:
                new_cw = [[B,G,R],[I,I,1,t-1,t,t]] #0,0,1,0,1,1
                Map[h][w].append(new_cw)
print(Map[100][100])
 

#cap = cv2.VideoCapture('1.JPEG')

frame2 = cv2.imread('1.JPEG')
#frame2 = hist_equalizer(frame2)
for h in range(H):
        for w in range(W):
                B = float(frame2[h,w,0])
                G = float(frame2[h,w,1])
                R = float(frame2[h,w,2])
                x = [B,G,R]
                I = B+G+R
                if find_match2(x,Map[h][w]) == True:
                    frame2[h,w,0] = 0
                    frame2[h,w,1] = 0
                    frame2[h,w,2] = 0
cv2.imshow('Frame',frame2)
cv2.imshow('First',frame)
cv2.imwrite('Final.jpg',frame2)
cv2.imwrite('First.jpg',frame)
end = time.time()
print(end-start)
cv2.waitKey(0)
cv2.destroyAllWindows()

       
    