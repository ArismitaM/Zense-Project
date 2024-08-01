import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

img = rasterio.open('../data/archive/label/val/monrovia_17.tif')
img = rasterio.open('../data/archive/label/tarin/aachen_63.tif')

# To find the number of bands in the image
num_bands = img.count
@@ -21,25 +21,27 @@
        band_idxOfj = np.asarray(np.where(img_band == j))
        band_idxOfj_flipped = np.transpose(band_idxOfj)

        db_idxOfj_flipped = DBSCAN(eps=4, min_samples=20).fit(band_idxOfj_flipped)
        db_idxOfj_flipped = DBSCAN(eps=4, min_samples=45).fit(band_idxOfj_flipped)
        labels_idxOfj_flipped = db_idxOfj_flipped.labels_
        n_clusters_idxOfj_flipped = len(set(labels_idxOfj_flipped)) - (1 if -1 in labels_idxOfj_flipped else 0)
        n_noise_idxOfj_flipped = list(labels_idxOfj_flipped).count(-1)
        print(f"Clustering info for pixel value {j}:")
        print("Estimated number of clusters:", n_clusters_idxOfj_flipped)
        print("Estimated number of noise points:", n_noise_idxOfj_flipped)

        show(band_matrixj)
        plt.imshow(band_matrixj, origin='lower')
        #plt.show()
        #show(band_matrixj)

        # Hot vector plot (Unflipped)
        plt.title(f"Hot vector plot UnFlipped Pixel value: {j}")
        plt.scatter(band_idxOfj[1, :], band_idxOfj[0, :])
        plt.show()
        #plt.title(f"Hot vector plot UnFlipped Pixel value: {j}")
        #plt.scatter(band_idxOfj[1, :], band_idxOfj[0, :])
        #plt.show()

        # Hot vector plot (Flipped)
        plt.title(f"Hot vector plot Flipped Pixel value: {j}")
        plt.scatter(band_idxOfj_flipped[:, 1], band_idxOfj_flipped[:, 0])  # Swap x and y coordinates
        plt.show()
        #plt.title(f"Hot vector plot Flipped Pixel value: {j}")
        #plt.scatter(band_idxOfj_flipped[:, 1], band_idxOfj_flipped[:, 0])  # Swap x and y coordinates
        #plt.show()


        # Cluster plot
        plt.title(f"Cluster Plot Pixel value: {j}")
        unique_labels = set(labels_idxOfj_flipped)
        core_samples_mask = np.zeros_like(labels_idxOfj_flipped, dtype=bool)
        core_samples_mask[db_idxOfj_flipped.core_sample_indices_] = True
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                col = [0, 0, 0, 1]  # Black used for noise.
            class_member_mask = labels_idxOfj_flipped == k
            xy = band_idxOfj_flipped[class_member_mask & core_samples_mask]
            plt.plot(
                xy[:, 1],  # Swap x and y coordinates
                xy[:, 0],
                "o",
                markerfacecolor=tuple(col),
                markersize=3,
            )
            xy = band_idxOfj_flipped[class_member_mask & ~core_samples_mask]
            plt.plot(
                xy[:, 1],  # Swap x and y coordinates
                xy[:, 0],
                "o",
                markerfacecolor=tuple(col),
                markersize=1,
            )
        plt.show()
