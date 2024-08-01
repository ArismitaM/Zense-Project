import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle as box
import numpy as np
from sklearn.cluster import DBSCAN

img = rasterio.open('../data/archive/label/tarin/aachen_63.tif')
img = rasterio.open('../data/archive/label/val/monrovia_17.tif')

# To find the number of bands in the image
num_bands = img.count
print("Number of bands in the image =", num_bands)
for i in range(1, num_bands + 1):
    img_band = img.read(i)
    uniqueVals = np.unique(img_band)
    print("Unique Values:", uniqueVals)
    for j in uniqueVals:
        band_matrixj = np.copy(img_band)
        band_matrixj[band_matrixj != j] = 0
        band_idxOfj = np.asarray(np.where(img_band == j))
        band_idxOfj_flipped = np.transpose(band_idxOfj)

        db_idxOfj_flipped = DBSCAN(eps=4, min_samples=45).fit(band_idxOfj_flipped)
        db_idxOfj_flipped = DBSCAN(eps=4, min_samples=15).fit(band_idxOfj_flipped)
        #db_idxOfj_flipped = DBSCAN(eps=4, min_samples=43).fit(band_idxOfj_flipped)
        labels_idxOfj_flipped = db_idxOfj_flipped.labels_
        n_clusters_idxOfj_flipped = len(set(labels_idxOfj_flipped)) - (1 if -1 in labels_idxOfj_flipped else 0)
        n_noise_idxOfj_flipped = list(labels_idxOfj_flipped).count(-1)
        print(f"Clustering info for pixel value {j}:")
        print("Estimated number of clusters:", n_clusters_idxOfj_flipped)
        print("Estimated number of noise points:", n_noise_idxOfj_flipped)

        plt.imshow(band_matrixj, origin='lower')
        f, splots = plt.subplots(1,1)

        #plt.imshow(band_matrixj, origin='lower')
        #splots[0].imshow(band_matrixj, origin='lower')
        #plt.show()
        #show(band_matrixj)

        # Hot vector plot (Unflipped)
        #plt.title(f"Hot vector plot UnFlipped Pixel value: {j}")
        #plt.scatter(band_idxOfj[1, :], band_idxOfj[0, :])
        #plt.show()
        # Hot vector plot (Flipped)
        #plt.title(f"Hot vector plot Flipped Pixel value: {j}")
        #plt.scatter(band_idxOfj_flipped[:, 1], band_idxOfj_flipped[:, 0])  # Swap x and y coordinates
        #plt.show()
        # Cluster plot
        plt.title(f"Cluster Plot Pixel value: {j}")
        unique_labels = set(labels_idxOfj_flipped)
        # Create an array of all boolen false (zeros) of the shape of labels_idxOfj_flipped
        core_samples_mask = np.zeros_like(labels_idxOfj_flipped, dtype=bool)
        # Turn the locations of core
        core_samples_mask[db_idxOfj_flipped.core_sample_indices_] = True

        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                col = [0, 0, 0, 1]  # Black used for noise.

            class_member_mask = labels_idxOfj_flipped == k

            #print("Shape of cluster-turned-on: ", class_member_mask.shape)
            #print("Shape of band_idxOfj_flipped: ", band_idxOfj_flipped.shape)

            xy = band_idxOfj_flipped[class_member_mask & core_samples_mask]
            plt.plot(
            #print("Size of xy: ", xy.size)
            #print("Shape of xy: ", xy.shape)
            if (xy.size != 0):
                xmin = np.min(xy[:,1])
                ymin = np.min(xy[:,0])
                xmax = np.max(xy[:,1])
                ymax = np.max(xy[:,0])

                center_x = (xmin+xmax)/2
                center_y = (ymin+ymax)/2
                width = xmax-xmin
                height = ymax - ymin

                #print("cluster: ", xy)
                print("cluster min: ", xmin, ymin)
                print("cluster max: ", xmax, ymax)
                #print("cluster max: ", xy[xy.shape[0]-1,1], xy[xy.shape[0]-1,0])
                #boxRect = box((xmin, ymin), xmax-xmin, ymax-ymin, fc='none', ec=tuple(col), lw=5)
                boxRect = box((xmin, ymin), xmax-xmin, ymax-ymin, fc='none', ec='black', lw=5)
                splots.add_patch(boxRect)

            splots.plot(
                xy[:, 1],  # Swap x and y coordinates
                xy[:, 0],
                "o",
                markerfacecolor=tuple(col),
                markersize=3,
            )

            xy = band_idxOfj_flipped[class_member_mask & ~core_samples_mask]
            plt.plot(
            splots.plot(
                xy[:, 1],  # Swap x and y coordinates
                xy[:, 0],
                "o",
                markerfacecolor=tuple(col),
                markersize=1,
            )
        plt.show()
