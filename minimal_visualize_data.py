import dv_processing as dv
import cv2 as cv
from datetime import timedelta
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Visualize events from a file")
    parser.add_argument("-f", "--file", type=str, default="data/dvSave-2024_05_13_16_57_12.aedat4", help="Path to the file to visualize")
    parser.add_argument("-v", "--visualizer", action="store_true", help="Use visualizer instead of accumulator")
    parser.add_argument("-o", "--output", type=str, default="output.avi", help="Output video file")
    return parser.parse_args()

args = parse_args()

USE_VISUALIZER = args.visualizer # use either visualizer or accumulator to create image frames from events
OUTPUT_FILE = args.output
path_to_file = args.file

# Open a file
reader = dv.io.MonoCameraRecording(path_to_file)
# reader = dv.io.CameraCapture()

# Get and print the camera name that data from recorded from
print(f"data from camera: [{reader.getCameraName()}]")

# Initialize preview window
cv.namedWindow("Preview", cv.WINDOW_NORMAL)

# Initialize VideoWriter
resolution = reader.getEventResolution()
fourcc = cv.VideoWriter_fourcc(*'XVID')  # Codec, could be 'XVID', 'MJPG', etc.
fps = 30  # Frames per second
video_writer = cv.VideoWriter(OUTPUT_FILE, fourcc, fps, (resolution[0], resolution[1]))


# Make sure it supports event stream output, throw an error otherwise
if not reader.isEventStreamAvailable():
    raise RuntimeError("Input camera does not provide an event stream.")


# Initialize an accumulator with some resolution
accumulator = dv.Accumulator(reader.getEventResolution())

# Apply configuration, these values can be modified to taste
accumulator.setMinPotential(0.0)
accumulator.setMaxPotential(1.0)
accumulator.setNeutralPotential(0.1)
accumulator.setEventContribution(0.15)
accumulator.setDecayFunction(dv.Accumulator.Decay.EXPONENTIAL)
accumulator.setDecayParam(1e+6)
accumulator.setIgnorePolarity(False)
accumulator.setSynchronousDecay(False)

# Initialize a visualizer
visualizer = dv.visualization.EventVisualizer(reader.getEventResolution())


# Initialize a slicer
slicer = dv.EventStreamSlicer()

# callback method for slicer with accumulator
def preview_accumulator(events: dv.EventStore):
    # Pass events into the accumulator and generate a preview frame
    accumulator.accept(events)
    frame = accumulator.generateFrame()
    image = frame.image
    # extend the image to 3 channels for saving as video
    # image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = cv.merge([image, image, image])
    # Show the accumulated image
    cv.imshow("Preview", image)
    video_writer.write(image)
    cv.waitKey(2)

# callback method for slicer with visualizer
def preview_visualizer(events: dv.EventStore):
    image = visualizer.generateImage(events)
    cv.imshow("Preview", image)
    video_writer.write(image)
    cv.waitKey(2)



# Register a callback every 33 milliseconds

slicer_callback = preview_accumulator
if USE_VISUALIZER:
    slicer_callback = preview_visualizer

slicer.doEveryTimeInterval(timedelta(milliseconds=33), slicer_callback)
# slicer.doEveryTimeInterval(timedelta(milliseconds=33), preview_events)

# Run the event processing while the camera is connected
while reader.isRunning():
    # Receive events
    events = reader.getNextEventBatch()

    # Check if anything was received
    if events is not None:
        # If so, pass the events into the slicer to handle them
        slicer.accept(events)

video_writer.release()
cv.destroyAllWindows()