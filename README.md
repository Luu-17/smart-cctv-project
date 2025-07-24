# AI-Powered Smart CCTV for Safer Cities (SDG 11)

## 1. SDG Focus
- **Goal:** SDG 11 (Sustainable Cities and Communities), SDG 16 (Peace, Justice, and Strong Institutions)
- **Problem:** Urban areas face challenges in monitoring public safety and restricted zones due to limited human resources and inefficient manual surveillance.

## 2. AI Approach
- **Software Engineering Skills Applied:**
  - **Automation:** Uses YOLO-based object detection to automate surveillance and zone violation alerts.
  - **Testing:** (Add or mention unit/integration tests for detection and zone logic.)
  - **Scalability:** Modular code (separate config, detection, zone logic, recording).
- **Technical Solution:**
  - Deploy a real-time object detection model (YOLO) to monitor video feeds, detect people/vehicles, and alert on restricted zone violations.

## 3. Tools & Frameworks
- **AI/ML:** Ultralytics YOLO, OpenCV, NumPy
- **Software Engineering:** Git, Python, (optionally add Docker, CI/CD)
- **Data Sources:**
  - Public video datasets (for testing)
  - Real-time camera feeds

## 4. Deliverables
- **Code:** Well-documented Python scripts (recorder.py, detector.py, zone_detector.py, etc.)
- **Deployment:** Prototype runs locally; can be extended to web app or cloud.
- **Report:** Explains how automated surveillance supports safer, more sustainable cities (SDG 11).

## 5. Ethical & Sustainability Checks
- **Bias Mitigation:** (Can mention reviewing detection accuracy across diverse groups.)
- **Environmental Impact:** Uses lightweight YOLO models for efficiency.
- **Scalability:** Designed to run on low-resource hardware (e.g., Raspberry Pi, old PCs).

## 6. Sample Project Outline
| Phase        | Tasks                                                                 |
|--------------|-----------------------------------------------------------------------|
| Ideation     | Research urban safety challenges; brainstorm AI-powered surveillance. |
| Development  | Code detection, zone logic, recording; automate video management.     |
| Testing      | Validate detection accuracy; test zone violation logic.               |
| Deployment   | Run locally; (optionally) deploy on cloud or edge devices.            |
| Monitoring   | Collect feedback on system usability and detection accuracy.          |

## 7. Usage
- Run `python run.py` to start the Smart CCTV system.
- Draw restricted zones by clicking four points (any quadrilateral shape).
- Press 'c' to clear zones, 'i' for info, 'q' to quit.

## 8. Notes
- Zones must be redrawn each session (MVP behavior).
- For best performance, use a machine with a GPU or a lightweight YOLO model.

## 9. Future Enhancements
- Zone persistence (auto-save/load)
- Web dashboard
- Multi-camera support
- Cloud integration