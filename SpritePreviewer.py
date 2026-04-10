import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer


def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10)) if number_of_frames > 1 else 1

    for frame in range(number_of_frames):
        file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(file_name))

    return frames


class SpritePreview(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sprite Animation Preview")

        self.num_frames = 21
        self.frames = load_sprite("spriteImages", self.num_frames)

        self.current_frame = 0

        self.setupUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)


    def setupUI(self):
        frame = QFrame()

        self.label = QLabel()
        self.label.setPixmap(self.frames[0])

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        frame.setLayout(layout)
        self.setCentralWidget(frame)


    def update_frame(self):
        self.current_frame += 1

        if self.current_frame >= self.num_frames:
            self.current_frame = 0

        self.label.setPixmap(self.frames[self.current_frame])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpritePreview()
    window.show()
    sys.exit(app.exec_())