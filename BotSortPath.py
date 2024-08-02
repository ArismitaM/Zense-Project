import cv2
import numpy as np
import time
from pathlib import Path
from ultralytics import YOLO
from collections import defaultdict
from ultralytics.utils.plotting import Annotator
import socket

# Create a socket
s = socket.socket()

# Define the port to connect to
port = 5602
s.connect(('10.5.0.1', port))

# Initialize the model and other variables
model = YOLO("yolov8n.pt")
names = model.model.names
video_path = "/home/arismita/ML/SivaUncle/testing/test_videos/video97.mp4"

if not Path(video_path).exists():
    raise FileNotFoundError(f"Source path '{video_path}' does not exist.")

cap = cv2.VideoCapture(video_path)

# Command: gst-launch-1.0 -v filesrc location=/home/nvidia/FaceIT.mp4 ! qtdemux ! h264parse ! rtph264pay pt=96 config-interval=1 ssrc=10000000 mtu=1400 ! udpsink host=127.0.0.1 port=5602
gst_str_rtp = "appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5602"
gst_str_rtp = "qtdemux ! h264parse ! rtph264pay pt=96 config-interval=1 ssrc=10000000 mtu=1400 ! udpsink host=127.0.0.1 port=5602"
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Create videowriter as a SHM sink
out = cv2.VideoWriter(gst_str_rtp, 0, 30, (frame_width, frame_height), True)

start_time = time.time()
frame_count = 0

# Tracking history and PathID management
track_history = defaultdict(lambda: [])
path_id_mapping = {}
next_path_id = 0

highlight_track_id = None
highlight_duration = 10  # seconds

previous_visible_path_ids = set()

while cap.isOpened():
    success, frame = cap.read()

    if success:
        current_time = time.time()
        elapsed_time = current_time - start_time

        results = model.track(frame, persist=True)

        boxes = results[0].boxes.xywh.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        track_ids = results[0].boxes.id

        if track_ids is not None:
            track_ids = track_ids.int().cpu().tolist()
        else:
            track_ids = []

        annotator = Annotator(frame, line_width=2, example=str(names))
        
        visible_path_ids = []

        for box, track_id, cls in zip(boxes, track_ids, clss):
            x, y, w, h = box
            x1, y1, x2, y2 = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)

            # Assign a new PathID if the track_id is new
            if track_id not in path_id_mapping:
                path_id_mapping[track_id] = next_path_id
                next_path_id += 1

            path_id = path_id_mapping[track_id]
            visible_path_ids.append(path_id)
            label = f"{names[cls]} : {track_id} (PathID: {path_id})"

            # Check which TrackID to highlight
            if highlight_track_id is not None and track_id == highlight_track_id:
                color = (0, 255, 0)  # Green for highlight
            else:
                color = (218, 100, 255)  # Default color

            annotator.box_label([x1, y1, x2, y2], label, color)

            # Tracking Lines plot
            track = track_history[track_id]
            track.append((float(box[0]), float(box[1])))
            if len(track) > 30:
                track.pop(0)

            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [points], isClosed=False, color=(37, 255, 225), thickness=2)

            # Center circle
            cv2.circle(frame, (int(track[-1][0]), int(track[-1][1])), 5, (235, 219, 11), -1)

        current_visible_path_ids = set(visible_path_ids)
        if current_visible_path_ids != previous_visible_path_ids:
            path_ids_str = ",".join(map(str, current_visible_path_ids)) + '\r\n'
            s.send(path_ids_str.encode())
            previous_visible_path_ids = current_visible_path_ids

            # Receive data from the server
            try:
                data = s.recv(1024).decode()
                if data:
                    highlight_track_id = int(data.strip())
            except socket.timeout:
                pass  # Handle timeout if needed

        # cv2.imshow("YOLOv8 Detection", frame)
        out.write(frame)
        frame_count += 1

        #if cv2.waitKey(1) & 0xFF == ord("q"):
            # break
    else:
        break

end_time = time.time()
elapsed_time = end_time - start_time
fps = frame_count / elapsed_time

print(f"Processed {frame_count} frames in {elapsed_time:.2f} seconds.")
print(f"Frames per second (FPS): {fps:.2f}")

cap.release()
# cv2.destroyAllWindows()

# Close the connection
s.close()
