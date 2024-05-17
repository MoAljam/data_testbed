import dv_processing as dv
import cv2 as cv
from datetime import timedelta

use_live_feed = False
filename = "dvSave-2024_05_13_16_57_12.aedat4"
# Open the recording file
recording = dv.io.StereoCameraRecording(filename, "DVXplorer_DXA00463",
                                        "DVXplorer_DXA00462")

if use_live_feed:
    recording = dv.io.StereoCapture("DVXplorer_DXA00463", "DVXplorer_DXA00462")

# Initialize event accumulator with the known resolution
left_accumulator = dv.Accumulator(
    recording.getLeftReader().getEventResolution())
right_accumulator = dv.Accumulator(
    recording.getRightReader().getEventResolution())

# Create the preview windows
cv.namedWindow("Left", cv.WINDOW_NORMAL)
cv.namedWindow("Right", cv.WINDOW_NORMAL)

# Initialize a slicer
slicer = dv.StereoEventStreamSlicer()


# Declare the callback method for slicer
def slicing_callback(left, right):
    # Pass events into the accumulator and generate a preview frame
    left_accumulator.accept(left)
    left_frame = left_accumulator.generateFrame()
    right_accumulator.accept(right)
    right_frame = right_accumulator.generateFrame()

    # Show the accumulated image
    cv.imshow("Left", left_frame.image)
    cv.imshow("Right", right_frame.image)
    cv.waitKey(2)


# Register a callback every 33 milliseconds
slicer.doEveryTimeInterval(timedelta(milliseconds=33), slicing_callback)
left_events = recording.getLeftReader().getNextEventBatch()
right_events = recording.getRightReader().getNextEventBatch()
# Run the event processing while the camera is connected
while left_events is not None:
    slicer.accept(left_events, right_events)
    left_events = recording.getLeftReader().getNextEventBatch()
    right_events = recording.getRightReader().getNextEventBatch()
