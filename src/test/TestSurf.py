import numpy as np
import cv2
from matplotlib import pyplot as plt

'''
Created on 03/03/2016

@author: gustavo
'''

IMG_SOURCE1 = "../../resources/banheiro_fora_de_uso.png"
IMG_SOURCE2 = "../../resources/Banheiro_CIT.jpg"

if __name__ == '__main__':
    img1 = cv2.imread(IMG_SOURCE1,0)
    img2 = cv2.imread(IMG_SOURCE2,0)
    
    surf = cv2.xfeatures2d.SURF_create(10000)
    
    kp1, des1 = surf.detectAndCompute(img1,None)
    kp2, des2 = surf.detectAndCompute(img2,None)
    
    print len(kp1)
    print len(kp2)
    
    #imgRes1 = cv2.drawKeypoints(img1,kp1,None,(255,0,0),4)

    #imgRes2 = cv2.drawKeypoints(img2,kp2,None,(255,0,0),4)
    
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
    
    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches, None)
    
    plt.imshow(img3),plt.show()
