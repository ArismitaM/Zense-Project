# Path Tracking

## 📝 Overview

This part of the project is used for tracing the path of people. YOLOv8 has been used to for detecting people and alogorithms like BotSort and ByteTrack have been used for path tracking.

## 🪜 Steps involved in Tracking

- **Object Detection**
- **Unique ID Assignment:** After detection in the initial frame, each object will be assigned a unique ID to be used throughout the sequence of images or videos.
- **Motion Tracking:** The tracker will estimate the positions of each of the unique objects in the remaining images or frames to obtain the trajectories of each individual re-identified object.

## 📝 Difference in the Algos

### BoT-SORT‍
Based on DeepSORT, BOT-SORT modifies the state vector and other matrix parameters in the Kalman filter (KF) so that the prediction frame can better match the target.

### ByteTrack
Based on the mechanism of DeepSORT, ByteTrack requires the detector to put the detection boxes regardless of the score into the matching stage. For detection boxes with high scores, ByteTrack performs feature matching and IOU matching while those with low scores only perform IOU matching.

I tested the same video in both algorithms for comparitative analysis. 


## 🚘 Uses of Object Tracking

 It tracks an object or multiple objects in a sequence of images or videos, both spatially and temporally. It has great potential in making our lives more convenient. Some notable use cases include autonomous cars, where successful tracking of objects in the car’s vicinity is crucial to ensuring a safe and smooth drive, and “Just Walk Out” stores, where customers can simply walk into a store, take what they need, and walk out.