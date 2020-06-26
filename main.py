import cv2
import numpy as np
from matplotlib import pyplot as plt
import collections
import shutil
from PIL import Image
import re
import imutils
import pytesseract
from imutils import contours
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
from helpers import NumberPlates
import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    
    #create a Object of All number plates
    cars = NumberPlates()
    
    dir = "./NumberPlates/"
    #reading numer plates from NumberPlates directory
    cars.readNumberPlatesList()

    for plate in cars.plates :
        print()

        columns = shutil.get_terminal_size().columns
        print("".center(columns, "~"))
        print("::: READING FILE :::".center(columns))
        print("FILE NAME    :::: "+plate)
        try :
            #STEP 1:: Binary Image Processing
            #original Image
            ori_img = cv2.imread(dir+plate)
            original_images = cv2.imread(dir+plate)
            result = ori_img

            #MonoChrome image
            mono_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
            
            #getting height and width
            height = mono_img.shape[0]
            width = mono_img.shape[1]
            kernel = np.ones((3, 3),np.uint8)
            
            # #STEP :: Thresholding
            res_img = cars.thresholding(mono_img, ori_img)

            # STEP :: Edge Detection and countour findings
            edges = cv2.Canny(res_img, height, width)
            
            result, crop, crop_res = cars.findPlate(res_img, ori_img, result)
            
            thresh = cv2.adaptiveThreshold(crop,255,1,1,11,2)
            thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
        
            contours, crop, crop_res = cars.markPlate(crop, crop_res)

            text = pytesseract.image_to_string(crop, config='--psm 11')
            text = re.sub(r"[\n\t\s]*", "", text)

            title = ["Original", "Plate", text]
            result_plt = [original_images, crop, crop_res]

            num = [231, 232, 233]
            for i in range(len(result_plt)):
                plt.subplot(num[i]),plt.imshow(result_plt[i], cmap = 'gray')
                plt.title(title[i]), plt.xticks([]), plt.yticks([])
            
            plt.suptitle("Summary " +plate)
            
            #uncomment below line to view each image
            
            # plt.show()
            print("PLATE IS     :::: " + text)
            print()
        except:
            print("Plate not found")