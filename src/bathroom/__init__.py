
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capta o video
    ret, frame = cap.read()

    # TODO: Fazer os tratamentos e reconhecimentos aqui - INIICIO
    
    
    
    # Fazer os tratamentos e reconhecimentos aqui - INIICIO
    

    # Mostra o resultado
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()