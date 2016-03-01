import numpy as np
import cv2

# abre o video
cap = cv2.VideoCapture(0)

#le o primeiro frame
ret,frame = cap.read()

#mostra o video
while(1):
    ret,frame = cap.read()
    
    if ret == True:
        frame = cv2.flip(frame,0)
        cv2.imshow('Frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
#libera as entradas
cap.release()
cv2.destroyAllWindows()
