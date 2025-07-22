from ultralytics import YOLO
from zone_detector import ZoneDetector
import cv2
from config import *

def detect_objects(frame, model, zone_detector=None):
    """
    Detect objects in frame and optionally check for restricted zone violations
    
    Args:
        frame: Input frame
        model: YOLO model
        zone_detector: Optional ZoneDetector instance for restricted zone checking
    
    Returns:
        detected_frame: Frame with detections drawn
        results: Detection results for further processing
    """

    # Perform tracking with the model using configured classes
    results = model.track(frame, classes=DETECTION_CLASSES)  # Tracking with configured classes

    # Draw results on the frame (if results exist)
    if results and hasattr(results[0], 'plot'):
        detected_frame = results[0].plot()  # Draw boxes, etc.
    else:
        detected_frame = frame.copy()
    
    # Check for restricted zone violations if zone detector is provided
    if zone_detector:
        triggered_zones = zone_detector.check_detections(results)
        zone_detector.draw_zones(detected_frame)
        
        # Add alert text if zones are triggered
        if triggered_zones:
            cv2.putText(detected_frame, "RESTRICTED ZONE VIOLATION!", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, ZONE_ALERT_COLOR, 3)
    
    return detected_frame, results