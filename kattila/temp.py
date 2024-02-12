import cv2 
import numpy as np 
import os

def getTemplate(image,i):
    r = cv2.selectROI("Select", image)
    cropped_image = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    cv2.imwrite(f"template{i}.jpg", cropped_image) 

def match(image, template):
    res = cv2.matchTemplate(image,template,cv2.TM_CCORR_NORMED)
    pt = np.max(res)
    x = 0
    y = 0
    for i in range(len(res)): 
        for j in range(len(res[0])): 
            if res[i][j] == pt:
                y = i
                x = j
                break

    return x,y,pt
    
#path = "/home/kattila/kahvicam/kahvikamera/kattila/tests/testdata/"
image = cv2.imread('kahvi.jpg')
getTemplate(image,1)
getTemplate(image,2)

template1 = cv2.imread('template1.jpg')
template2 = cv2.imread('template2.jpg')

t_d1, t_w1, t_h1 = template1.shape[::-1] 
t_d2, t_w2, t_h2 = template2.shape[::-1] 

x1,y1,pt1 = match(image, template1)
x2,y2,pt2 = match(image, template2)

cv2.rectangle(image, (x1,y1), (x1 + t_w1, y1 + t_h1), (0, 255, 0), 2) 
cv2.rectangle(image, (x2,y2), (x2 + t_w2, y2 + t_h2), (0, 0, 255), 2) 
half1 = (int(x1+(t_w1/2)),int(y1+t_h1))
half2 = (int(x2+(t_w2/2)),int(y2))
cv2.line(image, half1, half2, (255,0,0), 2)

cv2.imshow("Orig", image) 
cv2.waitKey(0) 
cv2.destroyAllWindows()