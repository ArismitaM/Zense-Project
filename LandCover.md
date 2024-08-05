# Land Cover Classification

## 📝 Overview

The satellite images used for training are images from Europe but in this case, the testing was done majorly on the satellite images of the Indian sub-continent. 
The images in the data set are in `.tif` format (geospatial satellite images) and the labels are present in colour-coded format for each class.
So, the layers in the labels were extracted for each class and the `DBScan` clustering technique was used to draw clusters. Then, bounding boxes were drawn around each cluster and the dimensions of the boxes were used to generate the labels for training in YOLO and RetinaNet models.

## 📊 Analyzing Dataset

I analyzed the [data set](https://www.kaggle.com/datasets/aletbm/global-land-cover-mapping-openearthmap).

Most of the satellite images obtained on a day-to-day basis are in `.tif` format as they allow finer details in the image as compared to `.jpg` or `.png`. And for such heavily zoomed-out images, the finer details matter a lot. Images in `.tif` format have transparency and can contain multiple files (layers) for a single image which is not the case in `.jpg` or `.png` images.

There are 3 directories under in the data - `test`, `train`, and `val` (stands for validation)
- **Training set:** Used to train the model.
- **Validation set:** Used to evaluate the model during training and tune hyperparameters.
- **Test set:** Used to evaluate the model's performance after training is complete.

**This is an image present in the dataset under the directory images/train**

![Screenshot from 2024-05-18 19-19-43](https://github.com/ArismitaM/Zense-Project/blob/main/images/p1%20(1).png)

**Each image has 3 layers (RGB), so below are the layers of the above image:**

Red Channel
![Screenshot from 2024-05-18 19-20-01](https://github.com/ArismitaM/Zense-Project/blob/main/images/p2%20(1).png)

Green Channel
![Screenshot from 2024-05-18 19-20-09](https://github.com/ArismitaM/Zense-Project/blob/main/images/p3%20(1).png)

Blue Channel
![Screenshot from 2024-05-18 19-20-16](https://github.com/ArismitaM/Zense-Project/blob/main/images/p4%20(1).png)

**There is a corresponding label/train which has 1 layer with coloured label**

Colour(Hex)  | Class|
-------------|----------|
#800000	     |	Bareland |
#00FF24	     |	Rangeland |
#949494	     |	Developed space |
#FFFFFF	     |	Road |
#226126	     |	Tree |
#0045FF	     |	Water |
#4BB549	     |	Agriculture land |
#DE1F07	     |	Building |

![Screenshot from 2024-05-18 19-20-38](https://github.com/ArismitaM/Zense-Project/blob/main/images/p5%20(1).png)

## 🧵 Clustering (using DBScan)

Label displaying class 2 (Rangeland)
![Screenshot from 2024-05-31 10-43-17](https://github.com/ArismitaM/Zense-Project/blob/main/images/p6%20(1).png)

Clusters drawn on the label using DBScan
![Screenshot from 2024-05-31 10-44-34](https://github.com/ArismitaM/Zense-Project/blob/main/images/p7%20(1).png)

Drawing bounding boxes around clusters
![Screenshot from 2024-06-01 11-00-27](https://github.com/ArismitaM/Zense-Project/blob/main/images/p8%20(1).png)

So, the `clustering.py` file draws clusters for each class and makes bounding boxes around them. The coordinates of the boxes are used to generate labels and these labels are converted into YOLO format for training.
The YOLO format labels are then converted into Pascal VOC format for RetinaNet training.

## 🚀 MODELS USED

 1.  **YOLOv5(You Only Look Once, version 5):** This model is chosen for land cover classification due to its high accuracy and efficiency. Designed for real-time classification, it is ideal for applications requiring quick and precise results. YOLOv5's CNN architecture effectively learns and identifies spatial patterns, ensuring robust classification of various land cover types. Its end-to-end learning approach simplifies the classification pipeline, enhancing performance and reliability.

 2. **RetinaNet:** RetinaNet is chosen for land cover classification due to its high accuracy and robustness. It is designed for real-time classification, making it ideal for applications requiring precise results. RetinaNet's Focal Loss function effectively handles class imbalance, ensuring accurate classification of diverse land cover types. Its deep learning architecture captures intricate spatial patterns, enhancing performance and reliability.

## 🧮  Exploratory Data Analysis Results

#### YOLOv5 Model:

![yolo_f1_curve](https://github.com/ArismitaM/DL-Simplified/blob/main/Global%20Land%20Cover%20Mapping%20using%20Image%20Processing/Images/yolo_F1_curve.png)

![yolo_confusion_matrix](https://github.com/ArismitaM/DL-Simplified/blob/main/Global%20Land%20Cover%20Mapping%20using%20Image%20Processing/Images/yolo_confusion_matrix.png)

![yolo_labels](https://github.com/ArismitaM/DL-Simplified/blob/main/Global%20Land%20Cover%20Mapping%20using%20Image%20Processing/Images/yolo_labels.jpg)

![yolo_results](https://github.com/ArismitaM/DL-Simplified/blob/main/Global%20Land%20Cover%20Mapping%20using%20Image%20Processing/Images/yolo_results.png)

#### RetinaNet Model:

![retinanet_epoch_loss](https://github.com/ArismitaM/DL-Simplified/blob/main/Global%20Land%20Cover%20Mapping%20using%20Image%20Processing/Images/retinanet_epoch_loss.png)

![retinanet_epoch_mAP](https://github.com/ArismitaM/DL-Simplified/blob/main/Global%20Land%20Cover%20Mapping%20using%20Image%20Processing/Images/retinanet_epoch_mAP.png)

![retinanet_regression_loss](https://github.com/ArismitaM/DL-Simplified/blob/main/Global%20Land%20Cover%20Mapping%20using%20Image%20Processing/Images/retinanet_regression_loss.png)

## 📈 Performance of the Models based on the Accuracy Scores
The evaluation metrics I used to assess the models were epoch loss

| Model      | Epoch Loss |
|------------|----------|
| YOLOv5    | 0.020     |
| RetinaNet    | 7.188 |

## 📢 Conclusion
Based on the results we can draw the following conclusions:
1. **YOLOv5:** The YOLOv5 model had an epoch loss of 0.020. This loss was lower compared to RetinaNet, hence it outperformed the RetinaNet model. I could use my GPU to train this model as it used 3.07GB out of the 4GB memory my system has. I was able to train with 5000 epochs on my terminal and 100 epochs in jupyter notebook.

2. **RetinaNet:** I was successfully able to train YOLO using my GPU. However, that was not the case with RetinaNet. My GPU ran out of memory so I had to train this model using CPU. It could train to a maximum of 10 epochs using the CPU. This had an epoch loss of 7.188. This was higher than the YOLOv5 model.

So, after comparing both models, the final decision is to use the YOLO model.

## 🏞️ Testing result
![Testing result on Village near India border](https://github.com/ArismitaM/Zense-Project/blob/main/images/b4.jpg)

#### Image sources (used for testing):
1. [Click here](https://www.thehansindia.com/news/national/china-has-built-a-fully-functional-village-in-doklam-754410)
2. [Click here](https://timesofindia.indiatimes.com/india/second-chinese-village-along-arunachal-border-sat-images/articleshow/87788526.cms)
