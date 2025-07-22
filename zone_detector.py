import cv2
import numpy as np
from typing import List, Tuple, Optional
from config import *

class RestrictedZone:
    """Class to represent a restricted zone"""
    def __init__(self, x1: int, y1: int, x2: int, y2: int, name: str = "Restricted Zone"):
        self.x1, self.y1 = min(x1, x2), min(y1, y2)
        self.x2, self.y2 = max(x1, x2), max(y1, y2)
        self.name = name
        self.is_triggered = False
        self.trigger_count = 0
        
    def contains_point(self, x: int, y: int) -> bool:
        """Check if a point is inside the restricted zone"""
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
    
    def contains_bbox(self, bbox: Tuple[int, int, int, int]) -> bool:
        """Check if a bounding box intersects with the restricted zone"""
        bbox_x1, bbox_y1, bbox_x2, bbox_y2 = bbox
        
        # Check if bounding box overlaps with restricted zone
        return not (bbox_x2 < self.x1 or bbox_x1 > self.x2 or 
                   bbox_y2 < self.y1 or bbox_y1 > self.y2)
    
    def draw(self, frame: np.ndarray, color: Tuple[int, int, int] = ZONE_ALERT_COLOR, thickness: int = 2):
        """Draw the restricted zone on the frame"""
        # Draw rectangle
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), color, thickness)
        
        # Draw label
        label = f"{self.name} (Triggered: {self.trigger_count})" if self.is_triggered else self.name
        cv2.putText(frame, label, (self.x1, self.y1 - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

class ZoneDetector:
    """Class to manage multiple restricted zones"""
    def __init__(self):
        self.zones: List[RestrictedZone] = []
        self.drawing_mode = False
        self.current_zone_start = None
        self.zone_counter = 1
        
    def add_zone(self, x1: int, y1: int, x2: int, y2: int, name: Optional[str] = None):
        """Add a new restricted zone"""
        if name is None:
            name = f"Zone {self.zone_counter}"
            self.zone_counter += 1
            
        zone = RestrictedZone(x1, y1, x2, y2, name)
        self.zones.append(zone)
        print(f"Added restricted zone: {name} at ({x1},{y1}) to ({x2},{y2})")
        
    def mouse_callback(self, event, x, y, flags, param):
        """Mouse callback for drawing zones"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.drawing_mode:
                # Start drawing a new zone
                self.drawing_mode = True
                self.current_zone_start = (x, y)
                print(f"Started drawing zone at ({x}, {y})")
            else:
                # Finish drawing the zone
                self.drawing_mode = False
                if self.current_zone_start:
                    start_x, start_y = self.current_zone_start
                    self.add_zone(start_x, start_y, x, y)
                    self.current_zone_start = None
                    print(f"Finished drawing zone at ({x}, {y})")
                    
    def check_detections(self, detections) -> List[RestrictedZone]:
        """Check if any detections are in restricted zones"""
        triggered_zones = []
        
        if detections and hasattr(detections[0], 'boxes') and detections[0].boxes is not None:
            boxes = detections[0].boxes
            if hasattr(boxes, 'xyxy') and boxes.xyxy is not None:
                for box in boxes.xyxy:
                    x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                    
                    for zone in self.zones:
                        if zone.contains_bbox((x1, y1, x2, y2)):
                            if not zone.is_triggered:
                                zone.is_triggered = True
                                zone.trigger_count += 1
                                print(f"⚠️  ALERT: Person detected in {zone.name}!")
                            triggered_zones.append(zone)
                        else:
                            zone.is_triggered = False
                            
        return triggered_zones
    
    def draw_zones(self, frame: np.ndarray):
        """Draw all zones on the frame"""
        for zone in self.zones:
            color = ZONE_ALERT_COLOR if zone.is_triggered else ZONE_NORMAL_COLOR
            zone.draw(frame, color)
            
        # Draw current zone being created
        if self.drawing_mode and self.current_zone_start:
            cv2.rectangle(frame, self.current_zone_start, 
                         (frame.shape[1] - 1, frame.shape[0] - 1), ZONE_DRAWING_COLOR, 2)
            cv2.putText(frame, "Drawing zone...", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, ZONE_DRAWING_COLOR, 2)
    
    def clear_zones(self):
        """Clear all zones"""
        self.zones.clear()
        self.zone_counter = 1
        print("All restricted zones cleared")
        
    def get_zone_info(self) -> str:
        """Get information about all zones"""
        if not self.zones:
            return "No restricted zones defined"
            
        info = "Restricted Zones:\n"
        for i, zone in enumerate(self.zones, 1):
            info += f"{i}. {zone.name}: ({zone.x1},{zone.y1}) to ({zone.x2},{zone.y2}) - Triggers: {zone.trigger_count}\n"
        return info 