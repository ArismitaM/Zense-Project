# Path Tracking

## 📝 Overview

This part of the project is used to trace people's paths. YOLOv8 has been used for detecting people and algorithms like BotSort and ByteTrack have been used for path tracking.

## 🪜 Steps involved in Tracking

- **Object Detection**
- **Unique ID Assignment:** After detection in the initial frame, each object will be assigned a unique ID to be used throughout the sequence of images or videos.
- **Motion Tracking:** The tracker will estimate the positions of each of the unique objects in the remaining images or frames to obtain the trajectories of each individual re-identified object.

## 📝 Difference in the Algos

### BoT-SORT‍
Based on DeepSORT, BOT-SORT modifies the state vector and other matrix parameters in the Kalman filter (KF) so that the prediction frame can better match the target.

### ByteTrack
Based on the mechanism of DeepSORT, ByteTrack requires the detector to put the detection boxes regardless of the score into the matching stage. For detection boxes with high scores, ByteTrack performs feature matching and IOU matching while those with low scores only perform IOU matching.

I tested the same video in both algorithms for comparative analysis.

**Bot Sort**
![Bot Sort](https://github.com/ArismitaM/Zense-Project/blob/main/images/Screenshot%20from%202024-07-31%2007-38-51.png)
The video takes 16.04 seconds to run with a 43.02 FPS.

**Byte Track**
![Byte Track](https://github.com/ArismitaM/Zense-Project/blob/main/images/Screenshot%20from%202024-07-31%2007-40-06.png)
This video takes 21.83 seconds to run with a 31.60 FPS.

This shows that the Bot-Sort Algorithm is faster in this case.
However, the difference in the quality of performance was negligible.
This is why I chose to continue with BotSort instead of ByteTrack.

## 🚘 Terminilogies

**IoU (Intersection over Union)** 

This method relies entirely on the detection results rather than the image itself. Intersection over union (IoU) is used to calculate the overlap rate between two frames. When IoU reaches the threshold, the two frames are considered to belong to the same track. Since this method relies solely on IoU, it assumes that every object is detected in every frame or that the "gap" in between is small and the distance between two detections is not too large, i.e. video frame rate is high. The IOU is calculated by: IOU(a, b) = (Area(a) Area(b)) (Area(a) Area(b)) 

**Deep SORT**

DeepSORT mainly uses the Kalman filter and the Hungarian algorithm for object tracking. Kalman filtering is used to predict the state of tracks in the previous frame in the current frame. The Hungarian algorithm associates the tracking frame tracks in the previous frame with the detection frame detections in the current frame and performs track matching by calculating the cost matrix.


