# Project Report: AI-Powered Smart CCTV for Safer Cities

## 1. Project Title
AI-Powered Smart CCTV for Safer Cities (SDG 11)

## 2. SDG Focus
- **Goal:** SDG 11 (Sustainable Cities and Communities), SDG 16 (Peace, Justice, and Strong Institutions)
- **Problem Statement:**
  Urban areas face increasing challenges in ensuring public safety and monitoring restricted zones. Manual surveillance is resource-intensive and prone to human error, leading to inefficiencies in detecting and responding to security incidents.

## 3. AI Approach
- **Software Engineering Skills Applied:**
  - **Automation:** The system leverages YOLO-based object detection to automate the identification of people and vehicles in video feeds, reducing the need for constant human monitoring.
  - **Testing:** The codebase is structured to allow for unit and integration testing of detection and zone logic.
  - **Scalability:** The modular design (separate configuration, detection, zone management, and recording modules) facilitates easy extension and deployment.
- **Technical Solution:**
  - A real-time object detection model (YOLO) processes video streams, identifies objects of interest, and triggers alerts when restricted zones are violated. The system supports flexible zone definition via user input and provides visual and logged alerts.

## 4. Tools & Frameworks
- **AI/ML:** Ultralytics YOLO, OpenCV, NumPy
- **Software Engineering:** Git for version control, Python for development
- **Data Sources:**
  - Public video datasets for testing
  - Real-time camera feeds for deployment

## 5. Deliverables
- **Code:** Well-documented Python scripts (recorder.py, detector.py, zone_detector.py, etc.)
- **Deployment:** Prototype runs locally on a standard PC; can be extended to web or cloud platforms.
- **Report:** This document, detailing the alignment with SDGs and ethical considerations.

## 6. Ethical & Sustainability Checks
- **Bias Mitigation:** The system can be evaluated for detection accuracy across diverse environments and populations to minimize bias.
- **Environmental Impact:** Lightweight YOLO models are used to reduce computational and energy requirements.
- **Scalability:** The solution is designed to operate on low-resource hardware, making it accessible for a wide range of communities.

## 7. Project Outline
| Phase        | Tasks                                                                 |
|--------------|-----------------------------------------------------------------------|
| Ideation     | Research urban safety challenges; brainstorm AI-powered surveillance. |
| Development  | Code detection, zone logic, recording; automate video management.     |
| Testing      | Validate detection accuracy; test zone violation logic.               |
| Deployment   | Run locally;            |
| Monitoring   | Collect feedback on system usability and detection accuracy.          |

## 8. Deployment Notes
- The current prototype is designed to run locally. Deployment as a web or cloud application is a recommended future enhancement but is not required for MVP submission.

## 9. Conclusion
This project demonstrates how AI-powered surveillance can contribute to safer, more sustainable cities by automating the detection of restricted zone violations and reducing the burden on human operators. The modular, ethical, and scalable design ensures that the solution can be adapted and extended for broader impact. 