import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from pdf_utils import render_pdf_page

class PDFWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Technician Assistant - PDF Viewer")
        layout = QVBoxLayout()
        pdf_path = "BeginnersGuide-4thEd-Eng_v2.pdf"
        label = render_pdf_page(pdf_path, 0)
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(800, 600)
