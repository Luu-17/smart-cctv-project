import cv2
import time
import os
from config import *

def test_camera_fps():
    """Test camera FPS to ensure proper timing"""
    print("=== Camera FPS Test ===")
    
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
    
    # Get camera properties
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Camera FPS: {actual_fps}")
    print(f"Resolution: {width}x{height}")
    print(f"Target FPS: {TARGET_FPS}")
    
    # Test frame capture timing
    frame_count = 0
    start_time = time.time()
    
    print("\nTesting frame capture for 5 seconds...")
    
    while frame_count < 150:  # Test for ~5 seconds at 30fps
        ret, frame = cap.read()
        if ret:
            frame_count += 1
            cv2.imshow("Camera Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    end_time = time.time()
    actual_duration = end_time - start_time
    measured_fps = frame_count / actual_duration
    
    print(f"\nTest Results:")
    print(f"Frames captured: {frame_count}")
    print(f"Actual duration: {actual_duration:.2f} seconds")
    print(f"Measured FPS: {measured_fps:.2f}")
    print(f"Expected FPS: {TARGET_FPS}")
    
    if abs(measured_fps - TARGET_FPS) < 5:
        print("✅ FPS is within acceptable range")
    else:
        print("⚠️  FPS differs significantly from target")
    
    cap.release()
    cv2.destroyAllWindows()

def test_video_playback(video_path):
    """Test video playback speed"""
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return
    
    print(f"\n=== Video Playback Test: {video_path} ===")
    
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    
    print(f"Video FPS: {fps}")
    print(f"Total frames: {frame_count}")
    print(f"Expected duration: {duration:.2f} seconds")
    
    # Play video and measure actual time
    start_time = time.time()
    frame_num = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow("Video Test", frame)
        frame_num += 1
        
        # Wait for proper frame timing
        if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
            break
    
    end_time = time.time()
    actual_duration = end_time - start_time
    
    print(f"\nPlayback Results:")
    print(f"Frames played: {frame_num}")
    print(f"Actual playback time: {actual_duration:.2f} seconds")
    print(f"Speed ratio: {actual_duration/duration:.2f}x")
    
    if abs(actual_duration - duration) < 1:
        print("✅ Playback speed is normal")
    else:
        print("⚠️  Playback speed is abnormal")
        if actual_duration < duration:
            print("   - Video is playing too fast (fast-forward)")
        else:
            print("   - Video is playing too slow")
    
    cap.release()
    cv2.destroyAllWindows()

def analyze_video_file(video_path):
    """Analyze video file properties in detail"""
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return
    
    print(f"\n=== Video File Analysis: {video_path} ===")
    
    cap = cv2.VideoCapture(video_path)
    
    # Get all video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    
    # Convert fourcc to string
    fourcc_str = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
    
    duration = frame_count / fps if fps > 0 else 0
    file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
    
    print(f"File size: {file_size:.2f} MB")
    print(f"Resolution: {width}x{height}")
    print(f"Codec: {fourcc_str}")
    print(f"FPS: {fps}")
    print(f"Frame count: {frame_count}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Bitrate: {(file_size * 8) / duration:.2f} Mbps")
    
    # Check for potential issues
    if fps <= 0:
        print("❌ Invalid FPS detected")
    if frame_count <= 0:
        print("❌ Invalid frame count detected")
    if duration <= 0:
        print("❌ Invalid duration detected")
    
    cap.release()

def list_recorded_videos():
    """List all recorded videos for testing"""
    if not os.path.exists(OUTPUT_FOLDER):
        print(f"Recordings folder not found: {OUTPUT_FOLDER}")
        return []
    
    videos = []
    for filename in os.listdir(OUTPUT_FOLDER):
        if filename.endswith(VIDEO_EXTENSION):
            videos.append(os.path.join(OUTPUT_FOLDER, filename))
    
    return videos

if __name__ == "__main__":
    print("Smart CCTV Video Speed Test")
    print("=" * 40)
    
    # Test camera FPS
    test_camera_fps()
    
    # Test recorded videos
    videos = list_recorded_videos()
    if videos:
        print(f"\nFound {len(videos)} recorded videos:")
        for i, video in enumerate(videos, 1):
            print(f"{i}. {os.path.basename(video)}")
        
        # Analyze the most recent video
        latest_video = max(videos, key=os.path.getctime)
        analyze_video_file(latest_video)
        
        # Test playback
        test_video_playback(latest_video)
    else:
        print("\nNo recorded videos found. Run recorder.py first to create test videos.") 