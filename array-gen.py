#array-gen.py
##IMPORTS
#
import barcode
from barcode import EAN13
from barcode.writer import ImageWriter

from PIL import Image, ImageOps
from numpy import asarray
import numpy as np
#
##IMPORTS

#Set image = image that will be opened
image = Image.open('MNIST_DS/1/img_1000.jpg').convert('L')
img = Image.open('MNIST_DS/1/img_1000.jpg')
#Converts the gray image to an array
data = np.asarray(image)
newdata = np.asarray(img)
#Print the array
print(data)
print(newdata)
