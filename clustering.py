import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

#img = rasterio.open('../data/archive/images/val/svaneti_1.tif')
#img = rasterio.open('../data/archive/label/train/svaneti_1.tif')
#img = rasterio.open('../data/archive/label/val/ica_10.tif')
#img = rasterio.open('../data/archive/images/val/ica_10.tif')
img = rasterio.open('../data/archive/label/train/aachen_63.tif')
img = rasterio.open('../data/archive/label/val/monrovia_17.tif')

# To find the number of bands in the image
num_bands = img.count
@@ -35,47 +31,45 @@

        show(band_matrixj)

        # Scatter plot
        # Hot vector plot (Unflipped)
        plt.title(f"Hot vector plot UnFlipped Pixel value: {j}")
        plt.scatter(band_idxOfj[1, :], band_idxOfj[0, :])
        plt.show()

        # Hot vector plot (Flipped)
        plt.title(f"Hot vector plot Flipped Pixel value: {j}")
        plt.scatter(band_idxOfj_flipped[:, 1], band_idxOfj_flipped[:, 0])
        plt.scatter(band_idxOfj_flipped[:, 1], band_idxOfj_flipped[:, 0])  # Swap x and y coordinates
        plt.show()


        # Cluster plot
        plt.title(f"Cluster Plot Pixel value: {j}")
        # Additional snippet for displaying all clusters
        unique_labels = set(labels_idxOfj_flipped)
        core_samples_mask = np.zeros_like(labels_idxOfj_flipped, dtype=bool)
        core_samples_mask[db_idxOfj_flipped.core_sample_indices_] = True

        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]
                col = [0, 0, 0, 1]  # Black used for noise.

            class_member_mask = labels_idxOfj_flipped == k

            xy = band_idxOfj_flipped[class_member_mask & core_samples_mask]
            plt.plot(
                xy[:, 1],  # Swap x and y coordinates
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                #markeredgecolor="k",
                markersize=3,
            )

            xy = band_idxOfj_flipped[class_member_mask & ~core_samples_mask]
            plt.plot(
                xy[:, 1],  # Swap x and y coordinates
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                #markeredgecolor="k",
                markersize=1,
            )

        plt.show()
