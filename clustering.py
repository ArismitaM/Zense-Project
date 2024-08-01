import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle as box
import numpy as np
from sklearn.cluster import DBSCAN
import os
from PIL import Image

# Function to convert to YOLO format
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

# Open image
img = rasterio.open('../data/archive/label/trialTrain/aachen_1.tif')

img = rasterio.open('../data/archive/label/val/monrovia_17.tif')

folder_path = "/home/arismita/ML/landCover/data/archive/labels_txt/train"
# Extract the full filename
full_filename = os.path.basename(img.name)  # img.name gives the file path used to open the image
# Extract the file name without extension
file_name_without_ext = os.path.splitext(full_filename)[0]
# Add .txt extension to create the new file name

# Define folder paths and create directories if necessary
folder_path = "/home/arismita/ML/landCover/data/archive/labels_txt/trailTrain"
os.makedirs(folder_path, exist_ok=True)

# Create file path for the text file
txt_file_name = f"{file_name_without_ext}.txt"
file_path = os.path.join(folder_path, txt_file_name)
# Ensure that the folder exists
os.makedirs(folder_path, exist_ok=True)

# Read image band
img_band = img.read(1)
uniqueVals = np.unique(img_band)
print("Unique Values:", uniqueVals)

# Loop through unique values in the band
for j in uniqueVals:
    band_matrixj = np.copy(img_band)
    band_matrixj[band_matrixj != j] = 0
    band_idxOfj = np.asarray(np.where(img_band == j))
    band_idxOfj_flipped = np.transpose(band_idxOfj)

    db_idxOfj_flipped = DBSCAN(eps=4, min_samples=15).fit(band_idxOfj_flipped)
    #db_idxOfj_flipped = DBSCAN(eps=4, min_samples=43).fit(band_idxOfj_flipped)
    labels_idxOfj_flipped = db_idxOfj_flipped.labels_
    n_clusters_idxOfj_flipped = len(set(labels_idxOfj_flipped)) - (1 if -1 in labels_idxOfj_flipped else 0)
    n_noise_idxOfj_flipped = list(labels_idxOfj_flipped).count(-1)
    unique_labels = set(labels_idxOfj_flipped)

    print(f"Clustering info for pixel value {j}:")
    #print("Estimated number of clusters:", n_clusters_idxOfj_flipped)
    #print("Estimated number of noise points:", n_noise_idxOfj_flipped)

    f, splots = plt.subplots(1,1)
    # Image dimensions for YOLO conversion
    img_width, img_height = img_band.shape[1], img_band.shape[0]

    # Cluster plot
    #plt.title(f"Cluster Plot Pixel value: {j}")
    unique_labels = set(labels_idxOfj_flipped)
    # Create an array of all boolen false (zeros) of the shape of labels_idxOfj_flipped
    core_samples_mask = np.zeros_like(labels_idxOfj_flipped, dtype=bool)
    # Turn the locations of core
    core_samples_mask[db_idxOfj_flipped.core_sample_indices_] = True

    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
    for k in unique_labels:
        if k == -1:
            col = [0, 0, 0, 1]  # Black used for noise.
            continue

        class_member_mask = labels_idxOfj_flipped == k
        xy = band_idxOfj_flipped[class_member_mask]

        xy = band_idxOfj_flipped[class_member_mask & core_samples_mask]
        #print("Size of xy: ", xy.size)
        #print("Shape of xy: ", xy.shape)
        if (xy.size != 0):
            xmin = np.min(xy[:,1])
            ymin = np.min(xy[:,0])
            xmax = np.max(xy[:,1])
            ymax = np.max(xy[:,0])
        if xy.size != 0:
            xmin = np.min(xy[:, 1])
            ymin = np.min(xy[:, 0])
            xmax = np.max(xy[:, 1])
            ymax = np.max(xy[:, 0])

            center_x = (xmin+xmax)/2
            center_y = (ymin+ymax)/2
            width = xmax-xmin
            height = ymax - ymin
            # Convert to YOLO format
            yolo_box = convert((img_width, img_height), (xmin, xmax, ymin, ymax))

            values_to_add = [j, center_x, center_y, width, height]
            values_to_add = [j, *yolo_box]

            with open(file_path, 'a') as file:  # 'a' mode is for appending, use 'w' to overwrite
            with open(file_path, 'a') as file:
                for value in values_to_add:
                    file.write(f"{value} ")
                file.write("\n")

            #print("cluster: ", xy)
            #print("cluster min: ", xmin, ymin)
            #print("cluster max: ", xmax, ymax)
            #print("cluster max: ", xy[xy.shape[0]-1,1], xy[xy.shape[0]-1,0])
            #boxRect = box((xmin, ymin), xmax-xmin, ymax-ymin, fc='none', ec=tuple(col), lw=5)
            #boxRect = box((xmin, ymin), xmax-xmin, ymax-ymin, fc='none', ec='black', lw=5)
            #splots.add_patch(boxRect)

        '''
        splots.plot(
            xy[:, 1],  # Swap x and y coordinates
            xy[:, 0],
            "o",
            markerfacecolor=tuple(col),
            markersize=3,
        )
        xy = band_idxOfj_flipped[class_member_mask & ~core_samples_mask]
        splots.plot(
            xy[:, 1],  # Swap x and y coordinates
            xy[:, 0],
            "o",
            markerfacecolor=tuple(col),
            markersize=1,
        )
        '''

    #plt.show()

print(f"Bounding boxes saved to {file_path}")
