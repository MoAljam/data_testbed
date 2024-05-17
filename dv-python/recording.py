import datetime
import os
import select
import sys

import cv2 as cv
import dv_processing as dv

filename = "t.aedat4"
capture = dv.io.CameraCapture()

# Event only configuration
config = dv.io.MonoCameraWriter.EventOnlyConfig(capture.getCameraName(),
                                                capture.getEventResolution())

# Create the writer instance, it will only have a single event output stream.
writer = dv.io.MonoCameraWriter(filename, config)

# Initialize visualizer instance which generates event data preview
visualizer = dv.visualization.EventVisualizer(capture.getEventResolution())

# Create the preview window
cv.namedWindow("Preview", cv.WINDOW_NORMAL)


def preview_events(event_slice):
    cv.imshow("Preview", visualizer.generateImage(event_slice))
    cv.waitKey(2)


slicer = dv.EventStreamSlicer()
slicer.doEveryTimeInterval(datetime.timedelta(milliseconds=33), preview_events)

while True:
    # non-blocking code to break loop (stop recording) when enter is pressed
    os.system('cls' if os.name == 'nt' else 'clear')
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = input()
        break
    events = capture.getNextEventBatch()
    if events is not None:
        slicer.accept(events)
        writer.writeEvents(events)
