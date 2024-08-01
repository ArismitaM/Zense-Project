import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt

img = rasterio.open('/home/arismita/ML/landCover/data/archive/images/train/tokyo_37.tif')
#img = rasterio.open('/home/arismita/ML/landCover/data/archive/label/train/tokyo_37.tif')
#img = rasterio.open('/home/arismita/ML/landCover/data/archive/label/train/aachen_63.tif')

print ("The opened file details: ", img)
print ("The read metadata: ", img.meta)
print ("The read shape: ", img.shape)
#data = img.read()
#print("The read data: ", data)
show(img)
# X and Y are supposed to be latitude and longitude if u have the right metadata 

full_img = img.read() #Note the three bands and the shape of image

# To find the no. of bands in an image
num_bands = img.count
print("Number of bands in the image = ", num_bands)

for i in range (1, num_bands + 1):
    img_band = img.read(i) #stands for the 1st band
    #print ("The read metadata1: ", img_band1.meta)
    show(img_band)
    print (img_band)

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
