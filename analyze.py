import cv2
import pytesseract
import sys
import PIL.Image as Image
import matplotlib.pyplot as plt
import numpy as np
from pyzbar.pyzbar import decode


#Arguments should follow this structure: [shop_name] [image_location]
if len(sys.argv) != 3:
    raise Exception("Invalid arguments passed!")
shop = sys.argv[1]
image = Image.open(sys.argv[2])

#plt.imshow(image)
#plt.show()

#Converts RGB PIL image to opencv BGR image
#https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
img = np.array(image)
img = img[:,:,::-1].copy()

#From https://stackoverflow.com/questions/69050464/zoom-into-image-with-opencv
def zoom_at(img, zoom=1, angle=0, coord=None):
    
    cy, cx = [ i/2 for i in img.shape[:-1] ] if coord is None else coord[::-1]
    
    rot_mat = cv2.getRotationMatrix2D((cx,cy), angle, zoom)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    
    return result


gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bImage = zoom_at(img, 4, coord=(image.size[0] * 0.13,image.size[1] * 0.85))
#plt.imshow(bImage)
#plt.show()

#Load barcode
print(decode(bImage))

gr = zoom_at(gr, 2.25, coord=(image.size[0] * 0.8, image.size[1] * 0.4))

kernel = np.ones((20,20),np.float32)/400
gray = cv2.filter2D(gr,-1,kernel)

#plt.imshow(gray)
#plt.show()
if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
match shop:
    #May be changed when needed
    case "Albert" | "Billa" | "Lidl" | "Kaufland" | "Globus":
        dataDict = pytesseract.image_to_data(gray, lang = 'eng',config="--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789", output_type= pytesseract.Output.DICT)
        #Find biggest size
        lastFoundArea = 0
        lastFoundIndex = -1
        for i in range(len(dataDict["text"])):
            if dataDict["text"][i].strip() == '':
                continue
            area = dataDict["width"][i] * dataDict["height"][i]
            if area > lastFoundArea:
                lastFoundArea = area
                lastFoundIndex = i
        if lastFoundIndex != -1:
            print(dataDict["text"][lastFoundIndex])
        else:
            print('Couldnt find valid word')
    case _:
        print("Invalid shop.")