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


#introduce array class
class array:
	def __init__(self,path):
		#declares a path to the image
		self.path = path
	
	#create print array method
	def printarray(self):
		#Set image = image that will be opened
		image = Image.open(self.path).convert('L')
		#Converts the gray image to an array
		data = np.asarray(image)
		#Return the array data
		print(data)

#introduce class to perform projections, and then concatenate into string
class projection:
	#declares a method to define the input array data
	def __init__(self,data):
		self.data = data
	
	#computes the sum of each row in array	
	def proj_0(self):
		proj_list = self.data
		#takes the sum of the rows (axis = 1)
		row_sum = np.sum(proj_list,axis=1)
		print("Projection (0 deg): \n" , row_sum , "\n")

	#computes the sum of each collumn in the array
	def proj_90(self):
		proj_list = self.data
		#takes the sum of each column	
		col_sum = np.sum(proj_list,axis=0)
		print("Projection (90 deg): \n", col_sum , "\n")


array1 = array("MNIST_DS/1/img_10076.jpg")
array1.printarray()
#array1 = array("MNIST_DS/1/img_1000.jpg")
#array1.printarray()
#array2 = array("MNIST_DS/1/img_10006.jpg")
#array2.printarray()
##Set image = image that will be opened
#image = Image.open('MNIST_DS/1/img_1000.jpg').convert('L')
##Converts the gray image to an array
#data = np.asarray(image)
##Print the array
#print(data)
