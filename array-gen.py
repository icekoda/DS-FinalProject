#array-gen.py
#IMPORTS

import barcode
from barcode import EAN13
from barcode.writer import ImageWriter

from PIL import Image
from numpy import asarray

#IMPORTS


image = Image.open('MNIST_DS/0/img_10007.jpg')

numpydata = asarray(image)

print(numpydata.shape)
