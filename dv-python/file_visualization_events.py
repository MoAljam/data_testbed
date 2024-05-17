import datetime

import cv2 as cv
import dv_processing as dv

use_live_feed = False
filename = "dvSave-2024_05_13_16_57_12.aedat4"
# Open the recording file
recording = dv.io.MonoCameraRecording(filename)

if use_live_feed:
    recording = dv.io.CameraCapture()

# Initialize visualizer instance which generates event data preview
visualizer = dv.visualization.EventVisualizer(recording.getEventResolution())

# Create the preview window
cv.namedWindow("Preview", cv.WINDOW_NORMAL)


def preview_events(event_slice):
    cv.imshow("Preview", visualizer.generateImage(event_slice))
    cv.waitKey(2)


# Create an event slicer, this will only be used events only camera
slicer = dv.EventStreamSlicer()
slicer.doEveryTimeInterval(datetime.timedelta(milliseconds=33), preview_events)

events = recording.getNextEventBatch()
# start read loop
while events is not None:
    slicer.accept(events)
    events = recording.getNextEventBatch()
