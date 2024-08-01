import numpy as np
import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt

#img = rasterio.open('/home/arismita/ML/landCover/data/archive/images/train/tokyo_37.tif')
img = rasterio.open('/home/arismita/ML/landCover/data/archive/label/train/tokyo_37.tif')
#img = rasterio.open('/home/arismita/ML/landCover/data/archive/label/train/tokyo_37.tif')

lst = []
for i in range (0,11):
    emp = []
    for j in range (0, 11):
        emp.append(255)
    lst.append(emp)

print ("The opened file details: ", img)
print ("The read metadata: ", img.meta)
print ("The read shape: ", img.shape)
#data = img.read()
#print("The read data: ", data)
show(img)
show(lst)
'''
# X and Y are supposed to be latitude and longitude if u have the right metadata 
full_img = img.read() #Note the three bands and the shape of image

# To find the no. of bands in an image
num_bands = img.count
print("Number of bands in the image = ", num_bands)

img_band = img.read(1) #stands for the 1st band
img_band = lst.read() #stands for the 1st band
#print ("The read metadata1: ", img_band1.meta)
show(img_band)
print(img_band.shape)
print(img.colorinterp[0])
#for i in range (1, 101):
 #   print (img_band[i])
print (img_band)
arr = np.array(img_band)
unique_elements = np.unique(arr) 
print(unique_elements) 
print(unique_elements)
print(list(zip(*np.where(img_band == 5))))
#print(output)
'''
