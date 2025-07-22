# ===== SMART CCTV SYSTEM CONFIGURATION =====
# Modify these settings to customize your system behavior

# Recording Settings
RESTART_INTERVAL_MINUTES = 1   # How often to restart recording (in minutes) - TESTING MODE
SAVE_INTERVAL_HOURS = 1        # How often to save and restart the entire system (in hours) - TESTING MODE

# File Management
OUTPUT_FOLDER = "recordings"   # Folder to store video files
ENABLE_DAILY_ORGANIZATION = True  # Automatically organize files into daily folders

# Detection Settings
ENABLE_ZONE_DETECTION = True   # Enable restricted zone detection
DETECTION_CLASSES = [0, 2]     # Classes to detect: 0=person, 2=car (modify as needed)

# Camera Settings
CAMERA_INDEX = "examples/Example Video (1).mp4"               # Camera device index (usually 0 for built-in webcam)
TARGET_FPS = 30.0              # Target frames per second for recording
# Video codec options (try different ones if playback issues occur):
VIDEO_CODEC = 'XVID'           # Primary: XVID (most reliable for normal playback)
# VIDEO_CODEC = 'mp4v'         # Alternative 1: mp4v (if XVID doesn't work)
# VIDEO_CODEC = 'H264'         # Alternative 2: H264 (if available)
VIDEO_EXTENSION = '.avi'       # Video file extension (use .avi with XVID)
# VIDEO_EXTENSION = '.mp4'     # Use .mp4 if using mp4v codec

# Model Settings
YOLO_MODEL_PATH = "yolo11n.pt" # Path to YOLO model file

# Zone Detection Settings
ZONE_ALERT_COLOR = (0, 0, 255)  # BGR color for triggered zones (Red)
ZONE_NORMAL_COLOR = (0, 255, 0) # BGR color for normal zones (Green)
ZONE_DRAWING_COLOR = (255, 0, 0) # BGR color for drawing zones (Blue)

# =========================================== 