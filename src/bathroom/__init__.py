#!/usr/bin/env python

import numpy as np
import cv2
from ObjectDetector import ObjectDetector

#------------ CONSTANTES - INICIO ------------

#Metodo que sera usado na comparacao do objeto
MATCH_METHOD = "sift"

#Caminho da imagem base de comparacao do objeto
IMG_SOURCE = "../../resources/banheiro_fora_de_uso.png"

#------------ CONSTANTES - FIM ------------

cap = cv2.VideoCapture(0)

while(True):
    # Capta o video
    retornoCam, frame = cap.read()
    
    # se nao conseguiu ler o video, sai
    if retornoCam is None:
        break
    
    # --- Tratamentos e Reconhecimentos - INICIO
    
    # Detectando o Objeto
    # TODO: esta muito lento. Verificar.
    detector = ObjectDetector(MATCH_METHOD,IMG_SOURCE)
    detector.detect_object(frame)
    
    #Detectando e Contando Pessoas
    # TODO: fazer tratamento
    
    # --- Tratamentos e Reconhecimentos - FIM
    

    # Mostra o resultado
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()