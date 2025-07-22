import cv2
import os
import datetime
import time
from ultralytics import YOLO
from detector import detect_objects
from zone_detector import ZoneDetector
from config import *

# ===== CONFIGURATION SECTION =====
# All settings are now imported from config.py
# Modify config.py to change system behavior
# =================================

def create_output_folder():
    """Create the output folder if it doesn't exist"""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output folder: {OUTPUT_FOLDER}")

def generate_filename():
    """Generate a unique filename with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_camera01{VIDEO_EXTENSION}"

def setup_zone_detection():
    """Setup zone detection with mouse callback"""
    zone_detector = ZoneDetector()
    
    # Create a window and set mouse callback
    cv2.namedWindow("Camera-01")
    cv2.setMouseCallback("Camera-01", zone_detector.mouse_callback)
    
    return zone_detector

def capture():
    """Capture video with object detection and save to folder"""
    # Create output folder
    create_output_folder()
    
    # Generate unique filename
    filename = generate_filename()
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    
    print(f"Starting new recording session: {filename}")
    
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    # Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
    
    # Get actual camera properties
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Camera FPS: {actual_fps}")
    print(f"Resolution: {width}x{height}")
    print(f"Using codec: {VIDEO_CODEC}")

    # Use a fixed, reliable FPS for recording
    recording_fps = 30.0  # Fixed at 30 FPS for consistent playback
    print(f"Recording FPS: {recording_fps}")

    fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC)
    out = cv2.VideoWriter(filepath, fourcc, recording_fps, (width, height))

    # Load YOLO model
    model = YOLO(YOLO_MODEL_PATH)
    
    # Setup zone detection if enabled
    zone_detector = None
    if ENABLE_ZONE_DETECTION:
        zone_detector = setup_zone_detection()
        print("Zone detection enabled!")
        print("Instructions:")
        print("  - Click and drag to draw restricted zones")
        print("  - Press 'c' to clear all zones")
        print("  - Press 'i' to show zone information")
        print("  - Press 'q' to quit recording")

    # Frame timing for consistent playback
    frame_interval = 1.0 / recording_fps
    start_time = time.time()
    frame_count = 0
    last_frame_time = start_time

    while cap.isOpened():
        current_time = time.time()
        
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break

        # Detect objects and check zones
        detected_frame, results = detect_objects(frame, model, zone_detector)

        # Display frame
        cv2.imshow("Camera-01", detected_frame)
        
        # Write frame to video
        out.write(detected_frame)
        
        frame_count += 1
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c') and zone_detector:
            zone_detector.clear_zones()
        elif key == ord('i') and zone_detector:
            print("\n" + zone_detector.get_zone_info())
        
        # Maintain consistent timing by sleeping if needed
        elapsed_since_last = current_time - last_frame_time
        if elapsed_since_last < frame_interval:
            sleep_time = frame_interval - elapsed_since_last
            time.sleep(sleep_time)
        
        last_frame_time = time.time()

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    # Calculate actual recording duration
    actual_duration = time.time() - start_time
    print(f"Recording session completed: {filename}")
    print(f"Frames recorded: {frame_count}")
    print(f"Actual duration: {actual_duration:.2f} seconds")
    print(f"Effective FPS: {frame_count/actual_duration:.2f}")

def organize_daily_footage():
    """Organize footage into daily folders"""
    if not ENABLE_DAILY_ORGANIZATION or not os.path.exists(OUTPUT_FOLDER):
        return
        
    # Get current date for folder naming
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    daily_folder = os.path.join(OUTPUT_FOLDER, current_date)
    
    # Create daily folder if it doesn't exist
    if not os.path.exists(daily_folder):
        os.makedirs(daily_folder)
        print(f"Created daily folder: {daily_folder}")
    
    # Move all video files from recordings folder to daily folder
    moved_count = 0
    for filename in os.listdir(OUTPUT_FOLDER):
        if filename.endswith(VIDEO_EXTENSION) and filename != current_date:
            source_path = os.path.join(OUTPUT_FOLDER, filename)
            dest_path = os.path.join(daily_folder, filename)
            
            try:
                os.rename(source_path, dest_path)
                moved_count += 1
                print(f"Moved: {filename} -> {daily_folder}")
            except Exception as e:
                print(f"Error moving {filename}: {e}")
    
    if moved_count > 0:
        print(f"Organized {moved_count} files into daily folder: {daily_folder}")
    else:
        print("No files to organize")

def main():
    """Main function with restart loop and daily save interval"""
    print("=== Smart CCTV Recording System ===")
    print(f"Configuration:")
    print(f"  - Recording restart interval: {RESTART_INTERVAL_MINUTES} minutes")
    print(f"  - Daily save interval: {SAVE_INTERVAL_HOURS} hours")
    print(f"  - Output folder: {OUTPUT_FOLDER}")
    print(f"  - Zone detection: {'Enabled' if ENABLE_ZONE_DETECTION else 'Disabled'}")
    print(f"  - Daily organization: {'Enabled' if ENABLE_DAILY_ORGANIZATION else 'Disabled'}")
    print(f"  - Video format: {VIDEO_CODEC} ({VIDEO_EXTENSION})")
    print(f"  - Press 'q' to quit any recording session")
    print("==================================")
    
    # Calculate intervals
    restart_interval_seconds = RESTART_INTERVAL_MINUTES * 60
    save_interval_seconds = SAVE_INTERVAL_HOURS * 3600
    
    # Track time for daily saves
    last_save_time = time.time()
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            current_time = time.time()
            
            print(f"\n=== Recording Cycle #{cycle_count} ===")
            print(f"Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Calculate time until next daily save
            time_until_save = save_interval_seconds - (current_time - last_save_time)
            if time_until_save > 0:
                hours_until_save = int(time_until_save / 3600)
                minutes_until_save = int((time_until_save % 3600) / 60)
                print(f"Time until next daily save: {hours_until_save}h {minutes_until_save}m")
            
            capture()
            
            # Check if it's time for daily save
            if current_time - last_save_time >= save_interval_seconds:
                print(f"\n🔄 DAILY SAVE INTERVAL REACHED ({SAVE_INTERVAL_HOURS} hours)")
                print("Organizing footage into daily folders...")
                organize_daily_footage()
                last_save_time = current_time
                print("Daily save completed. Starting fresh cycle...")
            else:
                # Regular restart interval
                print(f"Waiting {RESTART_INTERVAL_MINUTES} minutes before next recording cycle...")
                print("Press Ctrl+C to stop the system")
                
                # Wait for the specified interval
                time.sleep(restart_interval_seconds)
            
    except KeyboardInterrupt:
        print("\nSystem stopped by user")
        print("Organizing any remaining footage...")
        organize_daily_footage()
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Organizing any remaining footage...")
        organize_daily_footage()

if __name__ == "__main__":
    main()
