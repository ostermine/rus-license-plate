import re
import cv2
from cv2 import threshold
import numpy as np
import pytesseract
from imutils import contours


hsv_min = np.array((0, 54, 5), np.uint8)
hsv_max = np.array((187, 255, 253), np.uint8)

# tesseract fix
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR"'

# create image object
image = cv2.imread("example.jpg") 

# make grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# add some sharpness
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

contours123, _ = cv2.findContours( thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def showImage(pic):
    cv2.imshow("test", pic)
    cv2.waitKey()
    cv2.destroyAllWindows()

for cnt in contours123:
        rect = cv2.minAreaRect(cnt) # пытаемся вписать прямоугольник
        box = cv2.boxPoints(rect) # поиск четырех вершин прямоугольника
        box = np.int0(box) # округление координат
        area = int(rect[1][0]*rect[1][1]) # вычисление площади
        if area > 500:
            # cv2.drawContours(image,[box],0,(255,0,0),2) # рисуем прямоугольник
            x, y, w, h = cv2.boundingRect(cnt)
            img = image[y:y+h, x:x+w]
            result = pytesseract.image_to_string(img, lang="rus+eng")
            if len(result) > 1:
                print(result)
                showImage(img)
            else:
                continue


