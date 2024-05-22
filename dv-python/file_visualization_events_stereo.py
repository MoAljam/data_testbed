import datetime

import dv_processing as dv
import cv2 as cv

use_live_feed = False
filename = "dvSave-2024_05_13_16_57_12.aedat4"
# Open the recording file
recording = dv.io.StereoCameraRecording(filename, "DVXplorer_DXA00462",
                                        "DVXplorer_DXA00463")

if use_live_feed:
    recording = dv.io.StereoCapture("DVXplorer_DXA00462", "DVXplorer_DXA00463")


# Initialize visualizer instance which generates event data preview
left_visualizer = dv.visualization.EventVisualizer(
    recording.getLeftReader().getEventResolution())
right_visualizer = dv.visualization.EventVisualizer(
    recording.getRightReader().getEventResolution())

# Create the preview windows
cv.namedWindow("Left", cv.WINDOW_NORMAL)
cv.namedWindow("Right", cv.WINDOW_NORMAL)


def preview_events(event_slice):
    cv.imshow("Left", left_visualizer.generateImage(event_slice))
    cv.imshow("Right", right_visualizer.generateImage(event_slice))
    cv.waitKey(2)


# Create an event slicer, this will only be used events only camera
slicer = dv.StereoEventStreamSlicer()
slicer.doEveryTimeInterval(datetime.timedelta(milliseconds=33), preview_events)

left_events = recording.getLeftReader().getNextEventBatch()
right_events = recording.getRightReader().getNextEventBatch()
# Run the event processing while the camera is connected
while left_events is not None:
    slicer.accept(left_events, right_events)
    left_events = recording.getLeftReader().getNextEventBatch()
    right_events = recording.getRightReader().getNextEventBatch()
