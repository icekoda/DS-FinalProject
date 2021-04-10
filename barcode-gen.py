#barcode-gen.py

#######################################
#             Created By:	      #
#				      #
#	Daniel LoPresti (100748818)   #
#       Juan Gaviria    (100738545)   #
#				      #
#                For:                 #
#                                     #
#    Prof. Shahryar Rahnamayan, PEng  #
#    Data Structures Course Project   #
#        OntarioTech University       #
#            April 11, 2021           #
# 				      #
#######################################
##  The purpose of this project is to
# take input of a image path, find the
# image, and convert it into a barcode.
#   This will enable us to then convert
# all remaining images to barcodes, and
# then compare them, matching up the
# barcodes that are the most similar.

##IMPORTS
#
import barcode
from barcode import Code128
from barcode.writer import ImageWriter

from PIL import Image, ImageOps
from numpy import asarray
import numpy as np

import time
import os
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
		return data

#introduce class to perform projections, to be then concatenated into string
class projection:
	#declares a method to define the input array data
	def __init__(self,data):
		self.data = data
	
	#computes the sum of each row in array	
	def proj_0(self):
		proj_list = self.data
		#takes the sum of the rows (axis = 1)
		row_sum = np.sum(proj_list,axis=1)
		print("======================================== \n"
		      "Projection (0 deg): \n" , row_sum , "\n")
		return row_sum

	#computes the sum of each collumn in the array
	def proj_90(self):
		proj_list = self.data
		#takes the sum of each column	
		col_sum = np.sum(proj_list,axis=0)
		print("Projection (90 deg): \n", col_sum , "\n")
		return col_sum

	##Here we need to compute trace values with different offsets. Originally,
	## I was going to take the sum of each diagonal and add them to a list,
	## but I'm too lazy, and I need something to test the barcode output.

	##The point of using the trace values is so we have a semi-unique number
	## for the diagonal to further distinguish between images with similar 
	## row and column sum values

	##If we have time later, I can change these functions, and it will still
	## work with the barcode string output

	#computes the trace values #1	
	def proj_45(self):
		proj_list = self.data
		#sets the offset
		ofs = -1
		trace_sum = np.trace(proj_list,offset=ofs)
		print("Projection (trace" , ofs ,"): \n" , trace_sum , "\n")	
		return trace_sum

	#computes the trace values #2		
	def proj_135(self):
		proj_list = self.data
		#sets the offeset
		ofs = 2
		trace_sum = np.trace(proj_list,offset=ofs)
		print("Projection (trace" , ofs ,"): \n" , trace_sum , "\n")	
		return trace_sum

#initiates a class that will take an integer, and split up each digit
class expand:
	def __init__(self,integer):
		self.integer = integer
	
	def this(self):
		n = self.integer
		digits = [int(x) for x in str(n)]
		return digits
		
#initiates a class that calculates the threshold value for converting a value
# to binary. The threshold value is the average value of the list
class threshold:
	def __init__(self,slist):
		self.slist = slist	
	
	def returnn(self):
		average = []
		#iterates over the inputed array, and adds each value to a list
		for i in np.nditer(self.slist):
			average.append(int(i))	
		#takes the average of the new list
		averagesum = sum(average)/len(average)
		#returns the threshold value
		return averagesum

#converts the given list to binary after calulating theshold
class binary:
	def __init__(self,a):
		self.a = a

	#converts the input to binary by comparing each value to the threshold
	def returnn(self):
		this = threshold(self.a)
		thresholda = this.returnn()
		string = []
		for i in np.nditer(self.a):
			if int(i) > thresholda:
				string.append(1)
			else:
				string.append(0)	
		print(string)	
		return string
	
#initiates a class that will convert the array values to binary based on
# a threshold value
class convert:
	#takes array input
	def __init__(self,array,p0,p45,p90,p135):
		#declares each input variable, in this case, the projections	
		self.array = array
		self.p0 = p0
		self.p45 = p45
		self.p90 = p90
		self.p135 = p135
	
	#takes binary conversion, adds to a list, and then outputs string
	def returnn(self):
		#the diagonal projections are different, and need to be expanded
		p45e = expand(self.p45)
		p135e = expand(self.p135)
		

		p0 = binary(self.p0)
		p45 = binary(np.asarray(p45e.this()))
		p90 = binary(self.p90)
		p135 = binary(np.asarray(p135e.this()))
		
		print("p0: ")
		p0r = p0.returnn()
		print("p45: ")
		p45r = p45.returnn()	
		print("p90: ")
		p90r = p90.returnn()
		print("p135: ")
		p135r = p135.returnn()
	
		return p0r , p45r , p90r , p135r

#this class will take in the binary projections, concatenate them, and output a
# barcode
class barcode:
	def __init__(self,p0,p45,p90,p135,a,b):
		self.p0 = p0
		self.p45 = p45
		self.p90 = p90
		self.p135 = p135
		self.a = a
		self.b = b

	def returnn(self):
		joined = self.p0 + self.p90 + self.p45 + self.p135
		#concatenates the list values into one string
		string = ''.join(map(str,joined))
		path =  ("MNIST_DS/" + str(self.a) + "/b_" + str(self.a) + str(self.b) +".jpg")
		#outputs the string as a barcode
		with open(path,'wb') as f:
			Code128(string,writer=ImageWriter()).write(f)	
		return joined
	
#outputs the string for the barcode
class output:
	def __init__(self,path,a,b):
		self.path = path
		self.a = a
		self.b = b
	
	def returnn(self):
		#goes through all functions
		#initializes the array
		arrayinit = array(self.path)
		narray = arrayinit.printarray()
		arrayproj = projection(narray)

		p0 = arrayproj.proj_0()
		p45 = arrayproj.proj_45()
		p90 = arrayproj.proj_90()
		p135 = arrayproj.proj_135()
		
		#outputs the binary string for each projection
		this = convert(narray,p0,p45,p90,p135)
		p0,p45,p90,p135 = this.returnn()
		
		bc = barcode(p0,p45,p90,p135,a,b)
		code = bc.returnn()	
		print("PATH: " , self.path)

print("========================================== \n"
      "===         BARCODE GENERATOR          === \n"
      "==                                      == \n"
      "===              v. 1.0                === \n"
      "========================================== \n")
input("         Press enter to start. \n")
os.system('clear')

#this method will cycle through the paths and output a barcode for each image
a = 0
b = 0

while a <= 9:
	b = 0
	while b <= 9:
		dpath = output("MNIST_DS/" + str(a) + "/i_" + str(a) + str(b) +".jpg", a , b)
		dpath.returnn()
		b += 1
	a += 1
print("========================================= \n"
      "=      Barcode Generation Complete      = \n"
      "========================================= \n")
