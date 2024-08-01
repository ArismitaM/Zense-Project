import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.cm as cm

# Open the image file
#img = rasterio.open('../data/archive/images/val/svaneti_1.tif')
#img = rasterio.open('../data/archive/label/train/svaneti_1.tif')
#img = rasterio.open('../data/archive/label/val/ica_10.tif')
#img = rasterio.open('../data/archive/images/val/ica_10.tif')
img = rasterio.open('../data/archive/label/train/aachen_63.tif')
print("The opened file details: ", img)
print("The read metadata: ", img.meta)
print("The read shape: ", img.shape)

# Read the full image
full_img = img.read()  # Note the three bands and the shape of the image

# To find the number of bands in an image
# To find the number of bands in the image
num_bands = img.count
print("Number of bands in the image = ", num_bands)

# Initialize lists to store clustering results
all_band_data = []
all_labels = []
print("Number of bands in the image =", num_bands)

# Process each band
for i in range(1, num_bands + 1):
    img_band = img.read(i)
    uniqueVals = np.unique(img_band)
    print("Unique Values in band {}: {}".format(i, uniqueVals))

    print("Unique Values:", uniqueVals)
    for j in uniqueVals:
        band_matrixj = np.copy(img_band)
        band_matrixj[band_matrixj != j] = 0

        band_idxOfj = np.asarray(np.where(img_band == j))
        band_idxOfj_flipped = band_idxOfj.reshape(band_idxOfj.shape[1], band_idxOfj.shape[0])
        print("Shape of band= ", band_idxOfj.shape)
        print("Shape after flipping= ", band_idxOfj_flipped.shape)
        band_idxOfj_flipped = np.transpose(band_idxOfj)

        db_idxOfj_flipped = DBSCAN(eps=4, min_samples=20).fit(band_idxOfj_flipped)
        labels_idxOfj_flipped = db_idxOfj_flipped.labels_
        n_clusters_idxOfj_flipped = len(set(labels_idxOfj_flipped)) - (1 if -1 in labels_idxOfj_flipped else 0)
        n_noise_idxOfj_flipped = list(labels_idxOfj_flipped).count(-1)
        print(f"Clustering info for pixel value {j}:")
        print("Estimated number of clusters:", n_clusters_idxOfj_flipped)
        print("Estimated number of noise points:", n_noise_idxOfj_flipped)

        show(band_matrixj)

        # Perform DBSCAN clustering
        db_idxOfj = DBSCAN(eps=0.6, min_samples=30).fit(band_idxOfj_flipped)
        labels_idxOfj = db_idxOfj.labels_
        # Scatter plot
        plt.title(f"Hot vector plot UnFlipped Pixel value: {j}")
        plt.scatter(band_idxOfj[1, :], band_idxOfj[0, :])
        plt.show()

        # Store clustering results
        all_band_data.append(band_idxOfj_flipped)
        all_labels.append(labels_idxOfj)
        plt.title(f"Hot vector plot Flipped Pixel value: {j}")
        plt.scatter(band_idxOfj_flipped[:, 1], band_idxOfj_flipped[:, 0])
        plt.show()

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_idxOfj = len(set(labels_idxOfj)) - (1 if -1 in labels_idxOfj else 0)
        n_noise_idxOfj = list(labels_idxOfj).count(-1)
        print("Clustering info for pixel val:= {}".format(j))
        print("Estimated number of clusters: %d" % n_clusters_idxOfj)
        print("Estimated number of noise points: %d" % n_noise_idxOfj)

# Concatenate all band data and labels for plotting
all_band_data = np.concatenate(all_band_data, axis=0)
all_labels = np.concatenate(all_labels, axis=0)
        plt.title(f"Cluster Plot Pixel value: {j}")
        # Additional snippet for displaying all clusters
        unique_labels = set(labels_idxOfj_flipped)
        core_samples_mask = np.zeros_like(labels_idxOfj_flipped, dtype=bool)
        core_samples_mask[db_idxOfj_flipped.core_sample_indices_] = True

# Create the list of unique clusters
list_of_clusters = list(set(all_labels))
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]

# Set up the figure for plotting
fig = plt.figure(figsize=(13, 9), frameon=True, facecolor='lightgrey', edgecolor='black')
ax = fig.add_subplot(1, 1, 1)
plt.axis()
plt.xlim([-2.5, 0.2])
plt.ylim([-0.7, 3.3])
plt.xlabel("log PhiZ")
plt.ylabel("log RQI")
            class_member_mask = labels_idxOfj_flipped == k

# Define a color map
colors = matplotlib.colormaps.get_cmap(len(list_of_clusters))
            xy = band_idxOfj_flipped[class_member_mask & core_samples_mask]
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                #markeredgecolor="k",
                markersize=3,
            )

# Plot each cluster
for idx, cluster in enumerate(list_of_clusters):
    color = colors(idx)
    plt.scatter(
        all_band_data[all_labels == cluster, 0], all_band_data[all_labels == cluster, 1],
        s=10, color=color,
        marker='8',
        label=cluster + 1
    )
            xy = band_idxOfj_flipped[class_member_mask & ~core_samples_mask]
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                #markeredgecolor="k",
                markersize=1,
            )

ax.yaxis.tick_right()
ax.yaxis.set_ticks_position('both')
plt.legend(scatterpoints=1, loc='center left', bbox_to_anchor=(-0.4, 0.5))
plt.grid()
plt.show()
        plt.show()
