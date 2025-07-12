#!/usr/bin/env python3
import freenect
import cv2
import numpy as np
from collections import namedtuple

# Define namedtuple and points
Point = namedtuple("Point", ["x", "y"])

points = {
    "center":    Point(320, 240),
    "top_left":  Point(100, 100),
    "top_right": Point(380, 100),
    "bot_left":  Point(100, 380),
    "bot_right": Point(540, 380)
}

# Extract RGB video frame
def get_video():
    video = freenect.sync_get_video()[0]
    return cv2.cvtColor(video, cv2.COLOR_RGB2BGR)

# Extract full depth frame
def get_depth():
    return freenect.sync_get_depth()[0]  # keep it uint16 to preserve full range

# Extract depth values at specified points
def get_depth_at_points(points, depth_frame):
    values = {}
    for name, pt in points.items():
        x, y = pt
        if 0 <= y < depth_frame.shape[0] and 0 <= x < depth_frame.shape[1]:
            values[name] = int(depth_frame[y, x])
        else:
            values[name] = None
    return values

# Main loop
while True:
    frame = get_video()
    depth = get_depth()

    # Optional: visualize normalized depth
    vis_depth = cv2.convertScaleAbs(depth, alpha=255.0/2048.0)

    # Draw point markers
    for pt in points.values():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
        cv2.circle(vis_depth, pt, 5, (255), -1)

    # Get depth at each point
    depth_values = get_depth_at_points(points, depth)
    for name, value in depth_values.items():
        print(f"{name}: {value}", end=' | ')
    print()

    # Show images
    cv2.imshow('Video', frame)
    cv2.imshow('Depth', vis_depth)

    if cv2.waitKey(30) == 27:  # ESC to exit
        break

cv2.destroyAllWindows()
