import dv_processing as dv
import cv2 as cv
from datetime import timedelta

use_live_feed = False
filename = "dvSave-2024_05_13_16_57_12.aedat4"
# Open the recording file
recording = dv.io.MonoCameraRecording(filename)

if use_live_feed:
    recording = dv.io.CameraCapture()

# Initialize event accumulator with the known resolution
accumulator = dv.Accumulator(recording.getEventResolution())

# Initialize preview window
cv.namedWindow("Preview", cv.WINDOW_NORMAL)

# Initialize a slicer
slicer = dv.EventStreamSlicer()

# Declare the callback method for slicer
def slicing_callback(events: dv.EventStore):
    # Pass events into the accumulator and generate a preview frame
    accumulator.accept(events)
    frame = accumulator.generateFrame()

    # Show the accumulated image
    cv.imshow("Preview", frame.image)
    cv.waitKey(2)


# Register a callback every 33 milliseconds
slicer.doEveryTimeInterval(timedelta(milliseconds=33), slicing_callback)
events = recording.getNextEventBatch()
# Run the event processing while the camera is connected
while events is not None:
    slicer.accept(events)
    events = recording.getNextEventBatch()
