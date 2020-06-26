import os
import cv2
import numpy as np

class NumberPlates:
    def __init__(self):
        super().__init__()
        self.plates = []
    
    def readNumberPlatesList(self):
        for f in os.listdir('./NumberPlates'):
            if os.path.isfile(os.path.join('./NumberPlates', f)):
                self.plates.append(f)
    
    def thresholding(self, mono_img, ori_img):
        blur = cv2.GaussianBlur(mono_img,(5,5),0)
        _, mask = cv2.threshold(blur, thresh=210, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        img_mask = cv2.bitwise_and(mono_img, mask)

        hsv = cv2.cvtColor(ori_img, cv2.COLOR_BGR2HSV)
        h, s, v1 = cv2.split(hsv)
        lower_white = np.array([0,0,160], dtype=np.uint8)
        upper_white = np.array([255,40,255], dtype=np.uint8)

        res_mask = cv2.inRange(hsv, lower_white, upper_white)
        res_img = cv2.bitwise_and(v1, mono_img, mask=res_mask)
        
        return res_img

    def findPlate(self, res_img, ori_img, result):
        ori_contours, _ = cv2.findContours(res_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        t_contours = sorted(ori_contours, key = cv2.contourArea, reverse = True)[:5]

        NumberPlateCnt = None
        found = False
        lt, rb = [10000, 10000], [0, 0]
        
        crop = ori_img
        crop_res = crop
        # Calculate polygonal curve, see if it has 4 curve
        for c in t_contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.06 * peri, True)
            if len(approx) == 4:
                found = True
                NumberPlateCnt = approx
                break
        if found:
            cv2.drawContours(result, [NumberPlateCnt], -1, (255, 0, 255), 2)

            for point in NumberPlateCnt:
                cur_cx, cur_cy = point[0][0], point[0][1]
                if cur_cx < lt[0]: lt[0] = cur_cx
                if cur_cx > rb[0]: rb[0] = cur_cx
                if cur_cy < lt[1]: lt[1] = cur_cy
                if cur_cy > rb[1]: rb[1] = cur_cy

            cv2.circle(result, (lt[0], lt[1]), 2, (150, 200, 255), 2)
            cv2.circle(result, (rb[0], rb[1]), 2, (150, 200, 255), 2)

            crop = res_img[lt[1]:rb[1], lt[0]:rb[0]]
            crop_res = ori_img[lt[1]:rb[1], lt[0]:rb[0]]
        return [result, crop, crop_res]

    def markPlate(self, crop, crop_res):
        # Find the contours
        contours,hierarchy = cv2.findContours(crop,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        # For each contour, find the bounding rectangle and draw it
        characters = []

        for cnt in contours:
            if  cv2.contourArea(cnt) > 50:
                x,y,w,h = cv2.boundingRect(cnt)
                characters.append(crop[y:y+h,x:x+w])
                cv2.rectangle(crop_res,(x,y),(x+w,y+h),(0,255,0),2)
            
        return [contours, crop, crop_res]
        