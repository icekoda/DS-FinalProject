#Importing cv2 for reading images, importing os for accessing files, importing pyzbar for decoding image data
import cv2
import os
from pyzbar.pyzbar import decode
from PIL import Image, ImageOps
import time

#class that defines text colors
class bcolors:
	CYAN = '\033[96m'
	ENDC = '\033[0m'

#Create necessary variables
#Input barcode here, will be retrieved from barcode generator part
x = input("MNIST_DS/"f"{bcolors.CYAN}x{bcolors.ENDC}""/b_xy.jpg \n Please enter x: \n")
y = input("MNIST_DS/" + x + "/b_" + x + f"{bcolors.CYAN}y{bcolors.ENDC}"".jpg \n Please enter y: \n")

path = (f"{bcolors.CYAN}MNIST_DS/{bcolors.ENDC}" + x + f"{bcolors.CYAN}/b_{bcolors.ENDC}" + x + y + f"{bcolors.CYAN}.jpg{bcolors.ENDC}\n")
print("PATH: " ,path)
time.sleep(1)

inputBarcode= ("MNIST_DS/" + x +"/b_" + x + y + ".jpg")

barcodeList = []
directoryList = []

#Function to decode the barcode
def BarcodeReader(image):
    # read the image using cv2
    img = cv2.imread(image)

    # Decode the barcode image
    detectedBarcodes = decode(img)

    # If not detected then print the message
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:

        # Go through all the detected barcodes in image
        for barcode in detectedBarcodes:

            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect

            # Put the rectangle in image using
            # cv2 to highlight the barcode
            cv2.rectangle(img, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            if barcode.data != "":
                return barcode.data


#Function used to calculate hamming distance
def calculateHammingDist(inputBarcode,currentBarcode):
    #Initiliazing the hamming distance as a high number to allow first checked hamming distance to be assigned
    hammingDistance = 0
    #The count variable will serve as a temporary hamming distance for each comparisson

    for i in range(0, len(inputBarcode) -2):
        if inputBarcode[i] != currentBarcode[i]:
            hammingDistance += 1
    return hammingDistance

#Determines the smallest hamming distance
def smallestHammingDist(barcodeList):
    smallestHammingDist = 100
    mostSimilarBar = ""

    for code in barcodeList:
        if code.hammingDist < smallestHammingDist:
            smallestHammingDist = code.hammingDist
            mostSimilarBar = code.img
    return  mostSimilarBar

#Create Code object to have the image path, barcode, and hamming distance all in one place for each image
class Code:
    def __init__(self, img, barcode, hammingDist):
        self.img = img
        self.barcode = barcode
        self.hammingDist = hammingDist



#Create Code object for input barcode
inputBarcodeCode = Code(str(inputBarcode),str(BarcodeReader(inputBarcode)), 0)

#Put all folder directories in one list
for folder in os.listdir(r"MNIST_DS"):
    directoryList.append(r"MNIST_DS/" + str(folder))

if __name__ == "__main__":
    # Create Code object for each image
    for folder in directoryList:
        for file in os.listdir(folder):
            #Making sure only the barcode images are being compared
            if file.startswith("b"):
                fileBarcode = str(BarcodeReader(r"MNIST_DS/" + str(folder)[-1] + "/" + file))
                #Making sure the input image isn't being compared
                if calculateHammingDist(inputBarcodeCode.barcode,fileBarcode) != 0:
                    #Create objects for all images containing their directory path, barcode, and hamming distance and storing them in the object array
                    barcodeList.append(Code(str(file),fileBarcode,calculateHammingDist(inputBarcodeCode.barcode,fileBarcode)))

print("Input Barcode: " + inputBarcodeCode.img + "\nMost Similar Barcode: " + smallestHammingDist(barcodeList))
