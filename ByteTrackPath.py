import os
import cv2
import time
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from collections import defaultdict
from ultralytics.utils.plotting import Annotator

# Set CUDA_LAUNCH_BLOCKING for more detailed error messages
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

track_history = defaultdict(lambda: [])

model = YOLO("yolov8n.pt")
model.to("cuda")  # Change to GPU if intended

names = model.model.names
video_path = "/home/arismita/ML/SivaUncle/testing/test_videos/video97.mp4"

if not Path(video_path).exists():
    raise FileNotFoundError(f"Source path '{video_path}' does not exist.")

cap = cv2.VideoCapture(video_path)

start_time = time.time()
frame_count = 0

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model.track(frame, persist=True, tracker="bytetrack.yaml")

        boxes = results[0].boxes.xywh.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        track_ids = results[0].boxes.id

        if track_ids is not None:
            track_ids = track_ids.int().cpu().tolist()
        else:
            track_ids = []

        annotator = Annotator(frame, line_width=2, example=str(names))

        for box, track_id, cls in zip(boxes, track_ids, clss):
            x, y, w, h = box
            x1, y1, x2, y2 = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
            label = str(names[cls]) + " : " + str(track_id)
            annotator.box_label([x1, y1, x2, y2], label, (218, 100, 255))

            # Tracking Lines plot
            track = track_history[track_id]
            track.append((float(box[0]), float(box[1])))
            if len(track) > 30:
                track.pop(0)

            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [points], isClosed=False, color=(37, 255, 225), thickness=2)

            # Center circle
            cv2.circle(frame, (int(track[-1][0]), int(track[-1][1])), 5, (235, 219, 11), -1)

        cv2.imshow("YOLOv8 Detection", frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

end_time = time.time()
elapsed_time = end_time - start_time
fps = frame_count / elapsed_time

print("\n")
print(f"Processed {frame_count} frames in {elapsed_time:.2f} seconds.")
print(f"Frames per second (FPS): {fps:.2f}")

cap.release()
cv2.destroyAllWindows()
