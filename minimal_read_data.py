import dv_processing as dv
import numpy as np
import pandas as pd
import argparse
import time

# import scipy.io as sio
# import matplotlib.pyplot as plt

# TODO: batched preprocessing of data.
#          - read batches of costum size from the file / camera directly without loading all data to memory
 
def parse_args():
    parser = argparse.ArgumentParser(description="read data from a file")
    parser.add_argument("-f", "--file", type=str, default="data/dvSave-2024_05_13_16_57_12.aedat4", help="Path to the file to read data from")
    return parser.parse_args()
    

args = parse_args()

path_to_file = args.file

# Open a file
reader = dv.io.MonoCameraRecording(path_to_file)
# reading from camera is analogous to reading from file but with dv.io.CameraCapture instead

# Get and print the camera name that data from recorded from
print(f"data from camera: [{reader.getCameraName()}]")

# Check if event stream is available
if reader.isEventStreamAvailable():

    all_events = []
    while reader.isRunning():
        # Read batch of events
        events = reader.getNextEventBatch()
        # break
        if events is not None:
            all_events.append(events.numpy())
        else:
            time.sleep(0.001)

    all_events = np.hstack(all_events)
    print(f"all events shape: {all_events.shape}")
    # convert into 4d array
    all_events_mat = np.zeros((all_events.shape[0], 4))
    all_events_mat[:, 0] = all_events["timestamp"]
    all_events_mat[:, 1] = all_events["x"]
    all_events_mat[:, 2] = all_events["y"]
    all_events_mat[:, 3] = all_events["polarity"]
    print(f"all events mat shape: {all_events_mat.shape}")
    print(f"all events mat sample: {all_events_mat[0]}")
    # convert into pandas dataframe
    all_events_df = pd.DataFrame(all_events)
    print(f"all events df shape: {all_events_df.shape}")
    print(f"all events df sample: {all_events_df.head(2)}")
    # save as cvs / mat file if needed
    # ...

    # inspecting the EVENT STREAM 
    # get one batch of events
    reader.resetSequentialRead()

    # meta data
    timerange = reader.getTimeRange()
    duration = timerange[1] - timerange[0]
    print(f"timerange: {timerange}")
    print(f"duration: {duration}")
    print(f"stream names: {reader.getStreamNames()}")
    print(f"events resulution: {reader.getEventResolution()}")
    print(f"events Metadata {reader.getStreamMetadata('events')}")

    # get the events within a time range
    packet = reader.getEventsTimeRange(timerange[0], (timerange[0]+timerange[1])//2, "events")
    print(f"packet type: {type(packet)}, shape: {packet.numpy().shape}")

    events = reader.getNextEventBatch()
    print(f"type of events storage: {type(events)}")
    print(events)
    # get individual channels as numpy arrays from the EventStore object
    coords = events.coordinates()
    timestamps = events.timestamps()
    polarities = events.polarities()

    print("get the events-data as seperated numpy arrays from the EventStore object:")
    print(f"number of events: {events.size()}")
    print(f"shape of coordinates(pixels): {coords.shape}, of type: {coords.dtype}")
    print(f"shape of timestamps: {timestamps.shape}, of type: {timestamps.dtype}")
    print(f"shape of polarities: {polarities.shape}, of type: {polarities.dtype}")

# # Check if frame stream is available
# if reader.isFrameStreamAvailable():

# # Check if IMU stream is available
# if reader.isImuStreamAvailable():

# # Check if trigger stream is available
# if reader.isTriggerStreamAvailable():


