from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QSlider,
    QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
    QSizePolicy, QScrollArea
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import cv2
from processing import filters, adjustments
from rembg import remove
from PIL import Image, ImageOps
from utils import file_ops
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modular Photo Editor")
        self.resize(1100, 700)

        self.image = None
        self.original = None

        self.setup_ui()

    # ================= UI SETUP =================
    def setup_ui(self):
        self.create_image_display()
        sidebar_content = self.create_sidebar()
        scroll_area = self.create_scroll_area(sidebar_content)

        main_layout = QHBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # ---- Helper Methods ----

    def create_image_display(self):
        self.label = QLabel("Open an Image")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setStyleSheet("""
            background-color: #1e1e1e;
            color: white;
            font-size: 69px;
        """)

    def create_sidebar(self):
        layout = QVBoxLayout()

        # File buttons
        for text, slot in [("Open Image", self.open_image),
                        ("Save Image", self.save_image)]:
            btn = self.create_button(text)
            btn.clicked.connect(slot)
            layout.addWidget(btn)
        layout.addSpacing(20)

        # HSV sliders
        self.sliders = {}
        for name, min_val, max_val, default in [
            ("Hue Min", 0, 179, 0),
            ("Hue Max", 0, 179, 179),
            ("Sat Min", 0, 255, 0),
            ("Sat Max", 0, 255, 255),
            ("Val Min", 0, 255, 0),
            ("Val Max", 0, 255, 255)
        ]:
            layout.addWidget(QLabel(name))
            slider = self.create_slider(min_val, max_val, default)
            layout.addWidget(slider)
            self.sliders[name] = slider

        # Mask button
        self.mask_btn = self.create_button("Show Mask")
        self.mask_btn.clicked.connect(self.show_mask)
        layout.addWidget(self.mask_btn)
        layout.addSpacing(20)

        # Filters buttons
        for text, slot in [("Gray Background", self.apply_gray_background),
                        ("Grayscale", self.apply_grayscale),
                        ("Blur", self.apply_blur)]:
            btn = self.create_button(text)
            btn.clicked.connect(slot)
            layout.addWidget(btn)
        layout.addSpacing(20)

        # Brightness slider
        self.slider_label = QLabel("Brightness")
        self.slider_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.apply_brightness)
        layout.addWidget(self.slider)

        layout.addStretch()

        # Put everything inside a QWidget
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(layout)
        return sidebar_widget

    def create_scroll_area(self, content_widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        scroll_area.setFixedWidth(220)
        scroll_area.setStyleSheet("background-color: #2c2c2c;")
        return scroll_area
    
    def create_slider(self, min_val, max_val, default):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.valueChanged.connect(self.update_mask)
        return slider

    # ================= Styled Button =================
    def create_button(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #888;
            }
        """)
        return btn
    
    def show_mask(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        lower = np.array([
            self.h_min.value(),
            self.s_min.value(),
            self.v_min.value()
        ])

        upper = np.array([
            self.h_max.value(),
            self.s_max.value(),
            self.v_max.value()
        ])

        mask = cv2.inRange(hsv, lower, upper)

        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        self.display_image(mask_rgb)

    def update_mask(self):
        if self.image is None:
            return

        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        lower = np.array([
            self.sliders["Hue Min"].value(),
            self.sliders["Sat Min"].value(),
            self.sliders["Val Min"].value()
        ])
        upper = np.array([
            self.sliders["Hue Max"].value(),
            self.sliders["Sat Max"].value(),
            self.sliders["Val Max"].value()
        ])

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(self.image, self.image, mask=mask)
        self.display_image(result)

    # ================= File Operations =================
    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.image = file_ops.load_image(path)
            self.original = self.image.copy()
            self.display_image(self.image)

    def save_image(self):
        if self.image is not None:
            path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG (*.jpg);;PNG (*.png)")
            if path:
                file_ops.save_image(path, self.image)

    # ================= Display Function =================
    # Convert BGR to RGB, then to QImage, and display
    def display_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(
            self.label.width(),
            self.label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_pixmap)

    # ================= Image Processing =================
    def apply_grayscale(self):
        if self.image is not None:
            self.image = filters.grayscale(self.image)
            self.display_image(self.image)

    def apply_blur(self):
        if self.image is not None:
            self.image = filters.blur(self.image)
            self.display_image(self.image)

    def apply_brightness(self):
        if self.original is not None:
            value = self.slider.value()
            self.image = adjustments.adjust_brightness(self.original, value)
            self.display_image(self.image)
            
    def apply_gray_background(self):
        if self.image is not None:
            self.image = adjustments.process_gray_background(self.image)
            self.display_image(self.image)