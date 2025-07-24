import sys
import threading
import cv2
import mediapipe as mp
import pyttsx3
import fitz  # For PDF
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage

# ===================== PDF Renderer =====================
def render_pdf_page(pdf_path, page_num=0):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap()
    img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
    label = QLabel()
    label.setPixmap(QPixmap.fromImage(img))
    doc.close()
    return label

class PDFWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Technician Assistant - PDF Viewer")
        layout = QVBoxLayout()
        pdf_path = "BeginnersGuide.pdf"  # Change if needed
        label = render_pdf_page(pdf_path, 0)
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(800, 600)

# ===================== Voice Assistant =====================
engine = pyttsx3.init()

def speak_message(message):
    engine.say(message)
    engine.runAndWait()

# ===================== Hand Tracking (MediaPipe) =====================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def run_hand_tracking():
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.imshow("Hand Tracking (Press Q to Quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

# ===================== Gesture Logic (Key + Voice) =====================
def gesture_logic():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Gesture Camera (Press T for Thumbs-Up, Q to Quit)", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('t'):
            print("Thumbs-Up detected!")
            speak_message("Calling Support")
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# ===================== Main App =====================
def run_app():
    app = QApplication(sys.argv)
    window = PDFWindow()
    window.show()

    
    threading.Thread(target=run_hand_tracking, daemon=True).start()
    threading.Thread(target=gesture_logic, daemon=True).start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
