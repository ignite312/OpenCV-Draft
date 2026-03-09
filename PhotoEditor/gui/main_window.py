from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QSlider,
    QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
    QSizePolicy
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import cv2
from processing import filters, adjustments
from rembg import remove
from PIL import Image, ImageOps
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

        # ===== Image Display Area =====
        self.label = QLabel("Open an Image")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setStyleSheet("""
            background-color: #1e1e1e;
            color: white;
            font-size: 69px;
        """)

        # ===== Sidebar Layout =====
        sidebar_layout = QVBoxLayout()

        self.mask_btn = self.create_button("Show Mask")
        self.mask_btn.clicked.connect(self.show_mask)
        sidebar_layout.addWidget(self.mask_btn)

        self.h_min = self.create_slider(0,179,0)
        self.h_max = self.create_slider(0,179,179)

        self.s_min = self.create_slider(0,255,0)
        self.s_max = self.create_slider(0,255,255)

        self.v_min = self.create_slider(0,255,0)
        self.v_max = self.create_slider(0,255,255)

        sidebar_layout.addWidget(QLabel("Hue Min"))
        sidebar_layout.addWidget(self.h_min)

        sidebar_layout.addWidget(QLabel("Hue Max"))
        sidebar_layout.addWidget(self.h_max)

        sidebar_layout.addWidget(QLabel("Sat Min"))
        sidebar_layout.addWidget(self.s_min)

        sidebar_layout.addWidget(QLabel("Sat Max"))
        sidebar_layout.addWidget(self.s_max)

        sidebar_layout.addWidget(QLabel("Val Min"))
        sidebar_layout.addWidget(self.v_min)

        sidebar_layout.addWidget(QLabel("Val Max"))
        sidebar_layout.addWidget(self.v_max)

        # Buttons
        self.open_btn = self.create_button("Open Image")
        self.open_btn.clicked.connect(self.open_image)

        self.save_btn = self.create_button("Save Image")
        self.save_btn.clicked.connect(self.save_image)

        self.gray_btn = self.create_button("Grayscale")
        self.gray_btn.clicked.connect(self.apply_grayscale)

        self.blur_btn = self.create_button("Blur")
        self.blur_btn.clicked.connect(self.apply_blur)


        self.gray_bg_btn = self.create_button("Gray Background")
        self.gray_bg_btn.clicked.connect(self.apply_gray_background)

        # Brightness Slider
        self.slider_label = QLabel("Brightness")
        self.slider_label.setStyleSheet("color: white; font-size: 14px;")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.apply_brightness)

        # Add to sidebar
        sidebar_layout.addWidget(self.gray_bg_btn)
        sidebar_layout.addWidget(self.open_btn)
        sidebar_layout.addWidget(self.save_btn)

        sidebar_layout.addSpacing(20)

        sidebar_layout.addWidget(self.gray_btn)
        sidebar_layout.addWidget(self.blur_btn)

        sidebar_layout.addSpacing(20)

        sidebar_layout.addWidget(self.slider_label)
        sidebar_layout.addWidget(self.slider)

        sidebar_layout.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(220)
        sidebar_widget.setStyleSheet("background-color: #2c2c2c;")

        # ===== Main Layout =====
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

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
    def create_slider(self, min_val, max_val, default):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.valueChanged.connect(self.update_mask)
        return slider
    def update_mask(self):

        if self.image is None:
            return

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

        result = cv2.bitwise_and(self.image, self.image, mask=mask)

        self.display_image(result)
    # ================= File Operations =================
    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            self.image = cv2.imread(path) # Load in BGR format
            self.original = self.image.copy() # Keep original for adjustments
            self.slider.setValue(0) # Reset brightness slider
            self.display_image(self.image)

    def save_image(self):
        if self.image is not None:
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Image",
                "",
                "JPEG (*.jpg);;PNG (*.png)"
            )
            if path:
                cv2.imwrite(path, self.image)

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