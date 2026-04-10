# GitHub Repo: https://github.com/chloezhu26/sprite-previewer

import sys
import math
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QAction,
)


def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10)) if number_of_frames > 1 else 1

    for frame in range(number_of_frames):
        folder_and_file_name = (
            sprite_folder_name
            + "/sprite_"
            + str(frame).rjust(padding, "0")
            + ".png"
        )
        frames.append(QPixmap(folder_and_file_name))

    return frames


class SpritePreview(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sprite Animation Preview")

        self.num_frames = 21
        self.frames = load_sprite("spriteImages", self.num_frames)

        self.current_frame = 0
        self.current_fps = 1
        self.is_animating = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.setupUI()

    def setupUI(self):
        main_frame = QFrame()
        self.setCentralWidget(main_frame)

        outer_layout = QVBoxLayout()
        main_frame.setLayout(outer_layout)

        self.make_menu()

        content_widget = QWidget()
        content_layout = QHBoxLayout()
        content_widget.setLayout(content_layout)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(260, 260)
        self.image_label.setPixmap(self.scaled_current_pixmap())

        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(1)
        self.slider.setTickPosition(QSlider.TicksRight)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.change_fps)

        content_layout.addWidget(self.image_label, 1)
        content_layout.addWidget(self.slider)

        info_widget = QWidget()
        info_layout = QHBoxLayout()
        info_widget.setLayout(info_layout)

        self.fps_text_label = QLabel("Frames per second")
        self.fps_value_label = QLabel(str(self.current_fps))

        info_layout.addStretch()
        info_layout.addWidget(self.fps_text_label)
        info_layout.addSpacing(15)
        info_layout.addWidget(self.fps_value_label)
        info_layout.addStretch()

        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_widget.setLayout(button_layout)

        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.toggle_animation)

        button_layout.addStretch()
        button_layout.addWidget(self.start_stop_button)
        button_layout.addStretch()

        outer_layout.addWidget(content_widget)
        outer_layout.addWidget(info_widget)
        outer_layout.addWidget(button_widget)

        self.resize(500, 450)

    def make_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self.pause_animation)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(pause_action)
        file_menu.addAction(exit_action)

    def scaled_current_pixmap(self):
        pixmap = self.frames[self.current_frame]
        return pixmap.scaled(
            220,
            220,
            Qt.KeepAspectRatio,
            Qt.FastTransformation
        )

    def update_frame(self):
        self.current_frame += 1
        if self.current_frame >= self.num_frames:
            self.current_frame = 0

        self.image_label.setPixmap(self.scaled_current_pixmap())

    def change_fps(self, value):
        self.current_fps = value
        self.fps_value_label.setText(str(value))

        if self.is_animating:
            delay_in_ms = int(1000 / self.current_fps)
            self.timer.start(delay_in_ms)

    def toggle_animation(self):
        if self.start_stop_button.text() == "Start":
            delay_in_ms = int(1000 / self.slider.value())
            self.timer.start(delay_in_ms)
            self.is_animating = True
            self.start_stop_button.setText("Stop")
        else:
            self.timer.stop()
            self.is_animating = False
            self.start_stop_button.setText("Start")

    def pause_animation(self):
        self.timer.stop()
        self.is_animating = False
        self.start_stop_button.setText("Start")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpritePreview()
    window.show()
    sys.exit(app.exec_())