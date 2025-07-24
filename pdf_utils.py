import fitz
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage

def render_pdf_page(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap()
    img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
    label = QLabel()
    label.setPixmap(QPixmap.fromImage(img))
    doc.close()
    return label
