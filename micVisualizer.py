import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPen, QPainter, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal

import sounddevice as sd
import numpy as np


class SoundThread(QThread):
    volume_changed = pyqtSignal(int)

    def run(self):
        def print_sound(indata, outdata, frames, time, status):
            volume_norm = int(np.linalg.norm(indata) * 10)
            self.volume_changed.emit(volume_norm)

        with sd.Stream(callback=print_sound):
            while True:
                sd.sleep(10)  # sleep for 10 ms to avoid high CPU usage


class AudioVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        self.w, self.h = 50, 50  # size
        self.x_pos, self.y_pos = 50, 250  # coordinate

        self.pen = QPen()
        self.pen.setColor(Qt.green)
        self.pen.setWidth(3)

        self.resize(100, 300)

        #   sound render
        self.sound_thread = SoundThread()
        self.sound_thread.volume_changed.connect(self.on_volume_change)
        self.sound_thread.start()

    def on_volume_change(self, volume):
        self.h = -volume
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.drawRect(self.x_pos, self.y_pos, self.w, self.h)

        # coordinate line
        pen = QPen(Qt.black)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(self.x_pos - 30, 250, self.x_pos - 30, 0)

    def height(self):
        return self.geometry().height()

# start, without __name__ == "__main__" (maybe later)
app = QApplication(sys.argv)
visualizer = AudioVisualizer()
visualizer.show()
sys.exit(app.exec_())
