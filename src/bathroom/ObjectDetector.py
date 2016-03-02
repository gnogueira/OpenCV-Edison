import numpy as np
import cv2

'''
Created on 29 de fev de 2016

@author: gnogueira
'''

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    
    def init_feature(self, name):
        chunks = name.split('-')
        if chunks[0] == 'sift':
            detector = cv2.xfeatures2d.SIFT_create()
            norm = cv2.NORM_L2
        elif chunks[0] == 'surf':
            detector = cv2.xfeatures2d.SURF_create(800)
            norm = cv2.NORM_L2
        elif chunks[0] == 'orb':
            detector = cv2.ORB_create(400)
            norm = cv2.NORM_HAMMING
        elif chunks[0] == 'akaze':
            detector = cv2.AKAZE_create()
            norm = cv2.NORM_HAMMING
        elif chunks[0] == 'brisk':
            detector = cv2.BRISK_create()
            norm = cv2.NORM_HAMMING
        else:
            return None, None
        
        matcher = cv2.BFMatcher(norm)
        
        return detector, matcher    