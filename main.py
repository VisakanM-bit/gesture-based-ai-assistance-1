import sys
import threading
import pyttsx3
from PyQt5.QtWidgets import QApplication
from gui import PDFWindow
from gestures import run_hand_tracking

engine = pyttsx3.init()

def speak_message(message):
    engine.say(message)
    engine.runAndWait()

def gesture_logic():
    import cv2
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

def start_gesture_thread():
    gesture_logic()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFWindow()
    window.show()
    gesture_thread = threading.Thread(target=start_gesture_thread, daemon=True)
    gesture_thread.start()
    sys.exit(app.exec_())

