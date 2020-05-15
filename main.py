import cv2
import numpy as np
from matplotlib import pyplot as plt
import collections
from imutils import contours
import pytesseract

from helpers import NumberPlates

if __name__ == "__main__":
    
    #create a Object of All number plates
    cars = NumberPlates()
    
    dir = "./NumberPlates/"
    #reading numer plates from NumberPlates directory
    cars.readNumberPlates()
    cars.readAlphaNum()

    for plate in cars.plates :

        #STEP 1:: Binary Image Processing
        #original Image
        ori_img = cv2.imread(dir+plate)
        result = ori_img

        #MonoChrome image
        mono_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
        
        #getting height and width
        height = mono_img.shape[0]
        width = mono_img.shape[1]
        kernel = np.ones((2, 2),np.uint8)
        
        # #STEP :: Thresholding
        _, mask = cv2.threshold(mono_img, thresh=200, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        img_mask = cv2.bitwise_and(mono_img, mask)

        hsv = cv2.cvtColor(ori_img, cv2.COLOR_BGR2HSV)
        h, s, v1 = cv2.split(hsv)

        lower_white = np.array([0,0,160], dtype=np.uint8)
        upper_white = np.array([255,40,255], dtype=np.uint8)

        res_mask = cv2.inRange(hsv, lower_white, upper_white)
        res_img = cv2.bitwise_and(v1, mono_img, mask=res_mask)

        # STEP :: Edge Detection and countour findings
        edges = cv2.Canny(res_img, height, width)

        ori_contours, _ = cv2.findContours(res_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        t_contours = sorted(ori_contours, key = cv2.contourArea, reverse = True)[:5]

        NumberPlateCnt = None
        found = False
        lt, rb = [10000, 10000], [0, 0]
        
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

        #STEP :: Get Image answer
        

        #STEP :: Plotting

        title = [
            "Original",
            "img_mask",
            "res_img",
            "edges",
            "crop",
            "crop_res"
        ]
        result_plt = [
            ori_img,
            img_mask,
            res_img,
            edges,
            crop,
            crop_res
        ]

        num = [
            231,
            232,
            233,
            234,
            235,
            236
        ]
        for i in range(len(result_plt)):
            plt.subplot(num[i]),plt.imshow(result_plt[i], cmap = 'gray')
            plt.title(title[i]), plt.xticks([]), plt.yticks([])
        
        plt.suptitle("Summary " + plate)
        plt.show()
        # cv2.imshow("Original Image",crop)
        # cv2.waitKey()
        # break