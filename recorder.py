import cv2
from ultralytics import YOLO
from detector import detect_objects

def capture():
    cap = cv2.VideoCapture(0)

    # Force a safe FPS value
    fps = 20.0
    print(f"Using FPS: {fps}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('Camera-01-footage.avi', fourcc, fps, (width, height))

    # Load YOLO model once
    model = YOLO("yolo11n.pt")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detected_frame = detect_objects(frame, model)

        cv2.imshow("Camera-01", detected_frame)
        out.write(detected_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
