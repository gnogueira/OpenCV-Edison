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
    # Keypoints da imagem
    keypointImgObject = None
    # Descriptor da imagem
    descriptorImgObject = None  
    


    def __init__(self, method_name, imgObjectPath):
        '''
        Constructor
        '''
        try:
            self.imgObject = cv2.imread(imgObjectPath, 0)
        except:
            print "ERRO: Selecione a imagem para comparacao"
            raise
            sys.exit(1)     
        
        self.init_detector(method_name)
        # Calcula os keypoints e descriptors da imagem
        self.keypointImgObject, self.descriptorImgObject = self.detector.detectAndCompute(self.imgObject,None)
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
               
        keypointScene, descriptorScene = self.detector.detectAndCompute(imgScene, None)
        
        print 'img - %d features, scene - %d features' % (len(self.keypointImgObject), len(keypointScene))
        
        print 'Comparando...'
        raw_matches = self.matcher.knnMatch(self.descriptorImgObject, trainDescriptors = descriptorScene, k = 2)
        p1, p2, kp_pairs = self.filter_matches(self.keypointImgObject, keypointScene, raw_matches)
        if len(p1) >= 4:
            H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
            print '%d / %d  inliers/matched' % (np.sum(status), len(status))
        else:
            H, status = None, None
            print '%d matches found, not enough for homography estimation' % len(p1)
        
        # TODO: Terminar comparacao
        vis = self.explore_match("Janela", self.imgObject, imgScene, kp_pairs, status, H)
        
        
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
        
        
    def explore_match(self, win, img1, img2, kp_pairs, status = None, H = None):
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1+w2] = img2
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
    
        if H is not None:
            corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
            corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
            cv2.polylines(vis, [corners], True, (255, 255, 255))
    
        if status is None:
            status = np.ones(len(kp_pairs), np.bool_)
        p1 = np.int32([kpp[0].pt for kpp in kp_pairs])
        p2 = np.int32([kpp[1].pt for kpp in kp_pairs]) + (w1, 0)
    
        green = (0, 255, 0)
        red = (0, 0, 255)
        white = (255, 255, 255)
        kp_color = (51, 103, 236)
        for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
            if inlier:
                col = green
                cv2.circle(vis, (x1, y1), 2, col, -1)
                cv2.circle(vis, (x2, y2), 2, col, -1)
            else:
                col = red
                r = 2
                thickness = 3
                cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
                cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
                cv2.line(vis, (x2-r, y2-r), (x2+r, y2+r), col, thickness)
                cv2.line(vis, (x2-r, y2+r), (x2+r, y2-r), col, thickness)
        vis0 = vis.copy()
        for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
            if inlier:
                cv2.line(vis, (x1, y1), (x2, y2), green)
    
        cv2.imshow(win, vis)
        return vis
    