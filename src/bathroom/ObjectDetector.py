#!/usr/bin/env python

import numpy as np
import cv2

import sys, getopt

'''
Created on 29 de fev de 2016

@author: gnogueira
'''
from twisted.internet.process import detector

class ObjectDetector(object):
    '''
    classdocs
    '''
    detector = None
    matcher = None
    imgObject = None
    


    def __init__(self, method_name, imgObjectPath):
        '''
        Constructor
        '''
        try:
            self.imgObject = cv2.imread(imgObjectPath, 0)
        except:
            print "ERRO: Selecione a imagem para comparacao"
            sys.exit(1)     
        
        self.init_detector(method_name)
        if detector is None:
            print "ERRO: Selecione um metodo valido [sift/surf/orb/akaze/brisk]"
            sys.exit(1)               
        
        print "Usando metodo ", method_name
        
    
    def init_detector(self, method_name):
        
        chunks = method_name.split('-')
        if chunks[0] == 'sift':
            self.detector = cv2.xfeatures2d.SIFT_create()
            norm = cv2.NORM_L2
        elif chunks[0] == 'surf':
            self.detector = cv2.xfeatures2d.SURF_create(800)
            norm = cv2.NORM_L2
        elif chunks[0] == 'orb':
            self.detector = cv2.ORB_create(400)
            norm = cv2.NORM_HAMMING
        elif chunks[0] == 'akaze':
            self.detector = cv2.AKAZE_create()
            norm = cv2.NORM_HAMMING
        elif chunks[0] == 'brisk':
            self.detector = cv2.BRISK_create()
            norm = cv2.NORM_HAMMING
        
        if self.detector is not None:
            self.matcher = cv2.BFMatcher(norm)
    
    def detect_object(self, imgScene):
               
        kp1, desc1 = self.detector.detectAndCompute(self.imgObject,None)
        kp2, desc2 = self.detector.detectAndCompute(imgScene, None)
        
        print 'img1 - %d features, img2 - %d features' % (len(kp1), len(kp2))
        
        print 'Comparando...'
        raw_matches = self.matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2)
        p1, p2, kp_pairs = self.filter_matches(kp1, kp2, raw_matches)
        if len(p1) >= 4:
            H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
            print '%d / %d  inliers/matched' % (np.sum(status), len(status))
        else:
            H, status = None, None
            print '%d matches found, not enough for homography estimation' % len(p1)
        
        # TODO: Terminar comparacao
        #vis = explore_match(win, img1, img2, kp_pairs, status, H)
        
        
    def filter_matches(self, kp1, kp2, matches, ratio = 0.75):
        mkp1, mkp2 = [], []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append( kp1[m.queryIdx] )
                mkp2.append( kp2[m.trainIdx] )
        p1 = np.float32([kp.pt for kp in mkp1])
        p2 = np.float32([kp.pt for kp in mkp2])
        kp_pairs = zip(mkp1, mkp2)
        return p1, p2, kp_pairs
        
        
        
    