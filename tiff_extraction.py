import numpy as np
import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt

img = rasterio.open('/home/arismita/ML/landCover/data/archive/images/train/tokyo_37.tif')
#img = rasterio.open('/home/arismita/ML/landCover/data/archive/label/train/tokyo_37.tif')
#img = rasterio.open('/home/arismita/ML/landCover/data/archive/label/train/aachen_63.tif')
#img = rasterio.open('/home/arismita/ML/landCover/data/archive/images/train/tokyo_37.tif')
img = rasterio.open('/home/arismita/ML/landCover/data/archive/label/train/tokyo_37.tif')

print ("The opened file details: ", img)
print ("The read metadata: ", img.meta)
@@ -20,22 +20,17 @@
num_bands = img.count
print("Number of bands in the image = ", num_bands)

for i in range (1, num_bands + 1):
    img_band = img.read(i) #stands for the 1st band
    #print ("The read metadata1: ", img_band1.meta)
    show(img_band)
    print (img_band)
img_band = img.read(1) #stands for the 1st band
#print ("The read metadata1: ", img_band1.meta)
show(img_band)
print(img_band.shape)
print(img.colorinterp[0])
#for i in range (1, 101):
 #   print (img_band[i])

'''
fig = plt.figure(figsize=(10,10))
print("BEFORE AX1")
ax1 = fig.add_subplot(2,2,1)
ax1.imshow(img_band1,cmap='pink')
print("BEFORE AX2")
ax2 = fig.add_subplot(2,2,2)
ax2.imshow(img_band2,cmap='pink')
print("BEFORE AX3")
ax3 = fig.add_subplot(2,2,3)
ax3.imshow(img_band3,cmap='pink')
'''
arr = np.array(img_band)
unique_elements = np.unique(arr) 
print(unique_elements) 

print(list(zip(*np.where(img_band == 5))))
#print(output)
