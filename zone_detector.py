import cv2
import numpy as np
from typing import List, Tuple, Optional
from config import *
import json
import os

class RestrictedZone:
    """Class to represent a flexible (quadrilateral) restricted zone"""
    def __init__(self, points: List[Tuple[int, int]], name: str = "Restricted Zone"):
        if len(points) != 4:
            raise ValueError("A restricted zone must have exactly 4 points.")
        self.points = points  # List of 4 (x, y) tuples
        self.name = name
        self.is_triggered = False
        self.trigger_count = 0

    def contains_point(self, x: int, y: int) -> bool:
        # Use cv2.pointPolygonTest for point-in-polygon
        contour = np.array(self.points, dtype=np.int32)
        return cv2.pointPolygonTest(contour, (x, y), False) >= 0

    def contains_bbox(self, bbox: Tuple[int, int, int, int]) -> bool:
        # Check if any corner of the bbox is inside the polygon
        bbox_x1, bbox_y1, bbox_x2, bbox_y2 = bbox
        corners = [
            (bbox_x1, bbox_y1),
            (bbox_x2, bbox_y1),
            (bbox_x2, bbox_y2),
            (bbox_x1, bbox_y2)
        ]
        contour = np.array(self.points, dtype=np.int32)
        return any(cv2.pointPolygonTest(contour, pt, False) >= 0 for pt in corners)

    def draw(self, frame: np.ndarray, color: Tuple[int, int, int] = ZONE_ALERT_COLOR, thickness: int = 2):
        # Draw polygon
        pts = np.array(self.points, np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=thickness)
        # Draw label near the first point
        label = f"{self.name} (Triggered: {self.trigger_count})" if self.is_triggered else self.name
        cv2.putText(frame, label, (self.points[0][0], self.points[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

class ZoneDetector:
    """Class to manage multiple flexible restricted zones"""
    def __init__(self):
        self.zones: List[RestrictedZone] = []
        self.drawing_mode = False
        self.current_zone_points: List[Tuple[int, int]] = []
        self.zone_counter = 1

    def add_zone(self, points: List[Tuple[int, int]], name: Optional[str] = None):
        if name is None:
            name = f"Zone {self.zone_counter}"
            self.zone_counter += 1
        zone = RestrictedZone(points, name)
        self.zones.append(zone)
        print(f"Added restricted zone: {name} with points {points}")

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.drawing_mode:
                # Start drawing a new zone
                self.drawing_mode = True
                self.current_zone_points = [(x, y)]
                print(f"Started drawing zone at ({x}, {y})")
            else:
                self.current_zone_points.append((x, y))
                print(f"Added point ({x}, {y}) to current zone")
                if len(self.current_zone_points) == 4:
                    # Finish drawing the zone
                    self.drawing_mode = False
                    self.add_zone(self.current_zone_points)
                    self.current_zone_points = []
                    print(f"Finished drawing zone with 4 points")

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
        for zone in self.zones:
            color = ZONE_ALERT_COLOR if zone.is_triggered else ZONE_NORMAL_COLOR
            zone.draw(frame, color)
        # Draw current zone being created
        if self.drawing_mode and self.current_zone_points:
            pts = np.array(self.current_zone_points, np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=False, color=ZONE_DRAWING_COLOR, thickness=2)
            cv2.putText(frame, f"Drawing zone... ({len(self.current_zone_points)}/4)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, ZONE_DRAWING_COLOR, 2)

    def clear_zones(self):
        self.zones.clear()
        self.zone_counter = 1
        print("All restricted zones cleared")

    def get_zone_info(self) -> str:
        if not self.zones:
            return "No restricted zones defined"
        info = "Restricted Zones:\n"
        for i, zone in enumerate(self.zones, 1):
            info += f"{i}. {zone.name}: {zone.points} - Triggers: {zone.trigger_count}\n"
        return info 