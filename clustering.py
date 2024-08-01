import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.cm as cm

#img = rasterio.open('../data/archive/images/val/svaneti_1.tif')
#img = rasterio.open('../data/archive/label/train/svaneti_1.tif')
#img = rasterio.open('../data/archive/label/val/ica_10.tif')
#img = rasterio.open('../data/archive/images/val/ica_10.tif')
# Open the image file
img = rasterio.open('../data/archive/label/train/aachen_63.tif')
print ("The opened file details: ", img)
print ("The read metadata: ", img.meta)
print ("The read shape: ", img.shape)
#data = img.read()
#print("The read data: ", data)
#show(img)
# X and Y are supposed to be latitude and longitude if u have the right metadata 
print("The opened file details: ", img)
print("The read metadata: ", img.meta)
print("The read shape: ", img.shape)

full_img = img.read() #Note the three bands and the shape of image
# Read the full image
full_img = img.read()  # Note the three bands and the shape of the image

# To find the no. of bands in an image
# To find the number of bands in an image
num_bands = img.count
print("Number of bands in the image = ", num_bands)

for i in range (1, num_bands + 1):
    img_band = img.read(i) #stands for the 1st band
    #print ("The read metadata1: ", img_band1.meta)
    #show(img_band)
# Initialize lists to store clustering results
all_band_data = []
all_labels = []

# Process each band
for i in range(1, num_bands + 1):
    img_band = img.read(i)
    uniqueVals = np.unique(img_band)
    print("Unique Values: ", uniqueVals)
    print("Unique Values in band {}: {}".format(i, uniqueVals))

    for j in uniqueVals:
        band_idxOfj = np.asarray(np.where(img_band == j))
        band_idxOfj_flipped = band_idxOfj.reshape(band_idxOfj.shape[1], band_idxOfj.shape[0])
        print("Shape of band= ", band_idxOfj.shape)
        print("Shape after flipping= ", band_idxOfj_flipped.shape)
        #X_j = np.asarray([band_idxOfj[0,:], band_idxOfj[1.:])
        print ("uniqueVals: ", band_idxOfj)
        #print ("Shape of uniqueVals X: ", X_j.shape)

        # Perform DBSCAN clustering
        db_idxOfj = DBSCAN(eps=0.6, min_samples=30).fit(band_idxOfj_flipped)
        labels_idxOfj = db_idxOfj.labels_

        # Store clustering results
        all_band_data.append(band_idxOfj_flipped)
        all_labels.append(labels_idxOfj)

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_idxOfj = len(set(labels_idxOfj)) - (1 if -1 in labels_idxOfj else 0)
        n_noise_idxOfj = list(labels_idxOfj).count(-1)
        print("Clustering info for pixel val:= " % j)
        print("Clustering info for pixel val:= {}".format(j))
        print("Estimated number of clusters: %d" % n_clusters_idxOfj)
        print("Estimated number of noise points: %d" % n_noise_idxOfj)

        #print("Scatter Plot for pixel val = ", j)
        plt.title(j)
        plt.scatter(band_idxOfj[0,:], band_idxOfj[1,:])
        plt.show()
# Concatenate all band data and labels for plotting
all_band_data = np.concatenate(all_band_data, axis=0)
all_labels = np.concatenate(all_labels, axis=0)

# Create the list of unique clusters
list_of_clusters = list(set(all_labels))

# Set up the figure for plotting
fig = plt.figure(figsize=(13, 9), frameon=True, facecolor='lightgrey', edgecolor='black')
ax = fig.add_subplot(1, 1, 1)
plt.axis()
plt.xlim([-2.5, 0.2])
plt.ylim([-0.7, 3.3])
plt.xlabel("log PhiZ")
plt.ylabel("log RQI")

# Define a color map
colors = matplotlib.colormaps.get_cmap(len(list_of_clusters))

# Plot each cluster
for idx, cluster in enumerate(list_of_clusters):
    color = colors(idx)
    plt.scatter(
        all_band_data[all_labels == cluster, 0], all_band_data[all_labels == cluster, 1],
        s=10, color=color,
        marker='8',
        label=cluster + 1
    )

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
ax.yaxis.tick_right()
ax.yaxis.set_ticks_position('both')
plt.legend(scatterpoints=1, loc='center left', bbox_to_anchor=(-0.4, 0.5))
plt.grid()
plt.show()
