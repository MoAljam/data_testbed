import datetime
import os
import select
import sys

import cv2 as cv
import datetime
import dv_processing as dv
import cv2 as cv

filename = "t.aedat4"
# Open the cameras
camera = dv.io.StereoCapture("DVXplorer_DXA00462", "DVXplorer_DXA00463")

# Create the writer instance, it will only have a single event output stream.
writer = dv.io.StereoCameraWriter(filename, camera)

leftVis = dv.visualization.EventVisualizer(camera.left.getEventResolution())
rightVis = dv.visualization.EventVisualizer(camera.right.getEventResolution())

# Create the preview windows
cv.namedWindow("Left", cv.WINDOW_NORMAL)
cv.namedWindow("Right", cv.WINDOW_NORMAL)

slicer = dv.StereoEventStreamSlicer()

keepRunning = True

def preview(left, right):
    cv.imshow("Left", leftVis.generateImage(left))
    cv.imshow("Right", rightVis.generateImage(right))
    if cv.waitKey(2) == 27:
        global keepRunning
        keepRunning = False


slicer.doEveryTimeInterval(datetime.timedelta(milliseconds=33), preview)

while True:
    # non-blocking code to break loop (stop recording) when enter is pressed
    os.system('cls' if os.name == 'nt' else 'clear')
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = input()
        break
    left_events = camera.left.getNextEventBatch()
    right_events = camera.right.getNextEventBatch()
    # if reading fails, just pass an empty event store
    slicer.accept(left_events or dv.EventStore(),
                  right_events or dv.EventStore())
    if left_events is not None:
        writer.left.writeEvents(left_events)
    if right_events is not None:
        writer.right.writeEvents(right_events)
