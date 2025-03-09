import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPen, QPainter
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
        self.x_pos, self.y_pos = 50, 550  # coordinate
        self.pen = QPen()
        self.pen.setWidth(3)
        self.resize(100, 600)

        #   sound render
        self.sound_thread = SoundThread()
        self.sound_thread.volume_changed.connect(self.on_volume_change)
        self.sound_thread.start()

    def on_volume_change(self, volume):
        self.h = -volume
        self.update()
        if volume > 450:
            self.pen.setColor(Qt.red)
        else:
            self.pen.setColor(Qt.green)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.drawRect(self.x_pos, self.y_pos, self.w, self.h)

        # coordinate line
        pen = QPen(Qt.black)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(self.x_pos - 10, 550, self.x_pos - 10, 50)
        # small lines and values (bad code, beautiful view)
        for y in range(50, 551, 50):
            if y % 100 == 50:  # long line
                painter.drawLine(45, y, 40, y)
                if y >= 500:    # for beautiful display 0
                    painter.drawText(30, y + 5, str(500 - (y - 50)))
                else:
                    painter.drawText(20, y + 5, str(500 - (y - 50)))
            else:  # short line
                painter.drawLine(43, y, 40, y)
                if y >= 500:    # for beautiful display 50
                    painter.drawText(25, y + 5, str(500 - (y - 50)))
                else:
                    painter.drawText(20, y + 5, str(500 - (y - 50)))
#   maybe needed for further support of application:
    # def height(self):
    #     return self.geometry().height()


# start
app = QApplication(sys.argv)
visualizer = AudioVisualizer()
visualizer.show()
sys.exit(app.exec_())
