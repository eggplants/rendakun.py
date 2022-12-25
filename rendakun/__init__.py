from __future__ import annotations

import sys

from pyautogui import click
from PyQt6.QtCore import Qt, QThread, pyqtSlot
from PyQt6.QtGui import QFont, QIntValidator, QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

__version__ = "0.0.1"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(f"連打くん Version {__version__}")
        self.setStyleSheet("background-color: black;")
        self.rendakunWidget = Widget()
        self.setCentralWidget(self.rendakunWidget)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ms = 10
        self.thread: ClickThread | None = None  # type: ignore[assignment]
        self.initUI()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F9 and self.thread is None:
            self.labelA.setText("実行中")
            self.labelD.setText("F10で終了")
            self.thread = ClickThread(self.ms)
            self.thread.start()
        elif event.key() == Qt.Key.Key_F10 and self.thread is not None:
            self.labelA.setText("連打くん")
            self.labelD.setText("F9で開始")
            self.thread.stop()
            self.thread = None
        elif event.key() == Qt.Key.Key_Escape:
            if self.thread is not None:
                self.thread.stop()
            sys.exit(0)

    @pyqtSlot()
    def onInputFormChange(self) -> None:
        try:
            self.ms = int(self.inputForm.text())
        except ValueError:
            self.ms = 0

    def initUI(self) -> None:
        layout = QVBoxLayout()

        self.labelA = QLabel()
        self.labelA.setText("連打くん")
        font = QFont()
        font.setPointSize(64)
        font.setBold(True)
        self.labelA.setFont(font)
        self.labelA.setStyleSheet("QLabel { color : red; }")
        self.labelA.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.labelA)

        formLayout = QHBoxLayout()
        labelB = QLabel()
        labelB.setText("クリック間隔")
        labelB.setStyleSheet("QLabel { color : magenta; }")
        formLayout.addWidget(labelB)
        # |
        self.inputForm = QLineEdit()
        interval = QIntValidator()
        interval.setBottom(0)
        self.inputForm.setValidator(interval)
        self.inputForm.setText("10")
        self.inputForm.setStyleSheet("background-color: white;")
        self.inputForm.textChanged.connect(self.onInputFormChange)
        formLayout.addWidget(self.inputForm)
        # |
        labelC = QLabel()
        labelC.setText("（1秒=1000")
        labelC.setStyleSheet("QLabel { color : cyan; }")
        formLayout.addWidget(labelC)
        # |
        layout.addLayout(formLayout)

        self.labelD = QLabel()
        self.labelD.setText("F9で開始")
        self.labelD.setStyleSheet("QLabel { color : yellow; }")
        self.labelD.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.labelD)

        self.setLayout(layout)


class ClickThread(QThread):
    def __init__(self, ms: int) -> None:
        super().__init__()
        self.ms = ms
        self.isRunning: bool = False  # type: ignore[assignment]

    def run(self) -> None:
        self.isRunning = True
        while self.isRunning:
            click(button="left", clicks=1, interval=0)
            QThread.msleep(self.ms)

    def stop(self) -> None:
        self.isRunning = False


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        return app.exec()
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
