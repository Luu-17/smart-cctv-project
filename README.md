# Smart CCTV System

A comprehensive surveillance system with object detection, restricted zone monitoring, and automated footage management.

## Features

### 🎥 **Video Recording**
- Continuous video recording with configurable intervals
- Automatic restart every 10 minutes (configurable)
- Unique timestamp-based file naming to prevent overwriting
- Organized storage in daily folders

### 🔄 **24-Hour Save Interval**
- System runs continuously for 24 hours
- Automatically organizes footage into daily folders
- Restarts fresh every 24 hours for easy access to footage
- Configurable save interval in `config.py`

### 🚫 **Restricted Zone Detection**
- Draw custom restricted zones by clicking and dragging
- Real-time detection when people enter restricted areas
- Visual alerts with colored zones (green=normal, red=triggered)
- Zone violation counter and logging

### 🤖 **AI Object Detection**
- YOLO-based person and vehicle detection
- Real-time tracking and bounding box visualization
- Configurable detection classes (person, car, etc.)

### ⚙️ **Easy Configuration**
- All settings in `config.py` file
- No code modification required for basic customization
- Flexible timing and detection options

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install opencv-python ultralytics numpy
   ```

2. **Configure Settings** (optional)
   - Edit `config.py` to customize intervals, detection classes, etc.

3. **Run the System**
   ```bash
   python recorder.py
   ```

## Configuration

Edit `config.py` to customize:

```python
# Recording Settings
RESTART_INTERVAL_MINUTES = 10  # Recording restart interval
SAVE_INTERVAL_HOURS = 24       # Daily save interval

# Detection Settings
ENABLE_ZONE_DETECTION = True   # Enable restricted zones
DETECTION_CLASSES = [0, 2]     # 0=person, 2=car

# Camera Settings
CAMERA_INDEX = 0               # Camera device
FPS = 20.0                     # Recording FPS
```

## Usage Instructions

### **Zone Detection Controls**
- **Click and drag**: Draw restricted zones
- **'c' key**: Clear all zones
- **'i' key**: Show zone information
- **'q' key**: Quit recording session

### **System Behavior**
- **Recording cycles**: Restart every 10 minutes (configurable)
- **Daily saves**: Organize and restart every 24 hours (configurable)
- **File organization**: Automatic daily folder creation
- **Zone alerts**: Console notifications when zones are violated

## File Structure

```
smart-cctv-project/
├── recorder.py          # Main recording system
├── detector.py          # Object detection module
├── zone_detector.py     # Restricted zone detection
├── config.py           # Configuration settings
├── recordings/         # Video storage folder
│   ├── 2025-07-17/    # Daily folders
│   │   ├── 20250717_010626_camera01.avi
│   │   └── ...
│   └── ...
└── yolo11n.pt         # YOLO model file
```

## Features Summary

✅ **Non-destructive coding**: All original functionality preserved  
✅ **Folder storage**: Videos saved in organized daily folders  
✅ **No overwriting**: Timestamp-based unique filenames  
✅ **Restart loop**: Configurable recording intervals  
✅ **24-hour save**: Daily organization and system restart  
✅ **Restricted zones**: Click-to-draw zone detection  
✅ **Person detection**: Real-time AI-powered detection  
✅ **Easy configuration**: All settings in config file  
✅ **Visual alerts**: Color-coded zone status  
✅ **Console logging**: Detailed system status and alerts  

## Technical Details

- **Video Codec**: XVID (configurable)
- **Detection Model**: YOLO11n (configurable)
- **Frame Rate**: 20 FPS (configurable)
- **Resolution**: Auto-detected from camera
- **Storage**: AVI format with timestamp naming

## Troubleshooting

- **Camera not found**: Check `CAMERA_INDEX` in config.py
- **Model not loading**: Ensure `models/yolo11n.pt` is in project directory
- **Permission errors**: Check write permissions for recordings folder
- **Zone detection issues**: Ensure OpenCV window is active for mouse input

## Future Enhancements

- Email/SMS alerts for zone violations
- Web interface for remote monitoring
- Motion detection integration
- Cloud storage integration
- Multiple camera support

## Examples

See the `examples/` folder for sample scripts and usage demonstrations to help you get started with the Smart CCTV System. These examples show how to run detection on video files, test zone detection, and more.