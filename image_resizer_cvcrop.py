from PIL import Image, ImageOps
import os
import shutil
import cv2
import numpy as np;

if not os.path.exists('2000'):
    os.makedirs('2000')

if not os.path.exists('250'):
    os.makedirs('250')

if not os.path.exists('originals'):
    os.makedirs('originals')


for file in os.listdir('.'):
    if file.endswith('.jpg'):
        print(file)
        img = Image.open(file)
        fn, fext = os.path.splitext(file)

        #temp_img = img.copy()
        #temp_img.thumbnail((2000, 2000))
        #temp_img.save("2000/"+file,"JPEG",optimize=True,quality=85)


        img = cv2.imread(file, cv2.IMREAD_COLOR)
        img = cv2.bilateralFilter(img, 9,80,30)
        img = cv2.medianBlur(img, 41)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # threshold image

        #ret, threshed_img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        threshed_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 2)

        img_backtorgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        #w,h = img.shape[1::-1]
        #resized = cv2.resize(threshed_img, (int(w/5), int(h/5)))
        #cv2.imshow("contours", resized)


        # find contours
        contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #find the biggest area
        c = max(contours, key = cv2.contourArea)
        largest_contours = sorted(contours, key=cv2.contourArea)
        #largest contour is image, second largest is the object
        c = largest_contours[-2]

        x, y, w, h = cv2.boundingRect(c)
        #print(cv2.boundingRect(c))

        boundingMarginH = int(h*15/220)
        boundingMarginW = int(w*15/220)

        y = y - boundingMarginH
        x = x - boundingMarginW
        h = h + boundingMarginH*2
        w = w + boundingMarginW*2

        # draw the book contour (in green)
        cv2.rectangle(img_backtorgb, (x,y), (x+w, y+h), (0,128,0), 5)

        #w,h = img_backtorgb.shape[1::-1]
        #resized = cv2.resize(img_backtorgb, (int(w/5), int(h/5)))

        #cv2.imshow("contours", resized)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        temp_img = Image.open(file)
        cropped = temp_img.crop((x, y, x+w, y+h)) # left, upper, right, and lower pixel 


        print(cropped.size)

        #temp_img = img.copy()
        #temp_img = Image.fromarray(temp_img, 'RGB')
        cropped.thumbnail((4000, 250))
        cropped.save("250/"+file,"JPEG",optimize=True,quality=100)

        #shutil.move(file, 'originals/'+file)

print('\nDone!')






