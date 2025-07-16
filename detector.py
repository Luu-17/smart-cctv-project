from ultralytics import YOLO

def detect_objects(frame,model):

    # Load an official or custom model
    model = YOLO("yolo11n.pt")  # Load an official Detect model
    # model = YOLO("yolo11n-seg.pt")  # Load an official Segment model
    # model = YOLO("yolo11n-pose.pt")  # Load an official Pose model
    # model = YOLO("path/to/best.pt")  # Load a custom trained model

    # Perform tracking with the model
    results = model.track(frame, classes=[0,2])  # Tracking with default tracker
    # results = model.track("https://youtu.be/LNwODJXcvt4", show=True, tracker="bytetrack.yaml")  # with ByteTrack

    # Draw results on the frame (if results exist)
    if results and hasattr(results[0], 'plot'):
        detected_frame = results[0].plot()  # Draw boxes, etc.
        return detected_frame
    else:
        return frame