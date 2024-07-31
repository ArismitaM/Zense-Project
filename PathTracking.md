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

## 🚘 Uses of Object Tracking

 It tracks an object or multiple objects in a sequence of images or videos, both spatially and temporally. It has great potential to make our lives more convenient. Some notable use cases include autonomous cars, where successful tracking of objects in the car’s vicinity is crucial to ensuring a safe and smooth drive, and “Just Walk Out” stores, where customers can simply walk into a store, take what they need, and walk out.
