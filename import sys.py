import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QHBoxLayout
from PyQt5.QtCore import QTimer
import time
import random

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 500, 500)  # Set window geometry to 500x500 pixels

        self.power_button = QPushButton("Power On Camera", self)
        self.power_button.clicked.connect(self.start_recording)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.power_button)

    def start_recording(self):
        #camera recording starts here
        self.power_button.setEnabled(False)  # Disable the power button during recording

        self.loading_label = QLabel("Recording...", self)
        self.layout.addWidget(self.loading_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.record_for_10_seconds)
        self.timer.start(100)  # Start the timer to begin recording after 100 milliseconds

        self.record_start_time = time.time()

    def record_for_10_seconds(self):
        elapsed_time = time.time() - self.record_start_time
        progress_value = int((elapsed_time / 10) * 100)
        self.progress_bar.setValue(progress_value)

        if elapsed_time >= 10:
            self.timer.stop()
            self.loading_label.hide()
            self.progress_bar.hide()
            self.calculate_results()

    def calculate_results(self):
        #backend part of opencv and ml
        self.loading_label.setText("Calculating Results...")
        self.loading_label.show()

        self.progress_bar.setRange(0, 100)
        self.progress_bar.show()

        self.result_timer = QTimer(self)
        self.result_timer.timeout.connect(self.show_result)
        self.result_timer.start(50)  # Use a shorter interval for smoother progress updates

        self.result_start_time = time.time()

    def show_result(self):
        #show results here
        elapsed_time = time.time() - self.result_start_time
        progress_value = int((elapsed_time / 5) * 100)
        self.progress_bar.setValue(progress_value)

        if elapsed_time >= 5:
            self.result_timer.stop()
            self.loading_label.hide()
            self.progress_bar.hide()

            # Simulate background calculation
            time.sleep(2)

            result = random.randint(1, 100)
            result_label = QLabel(f"Random Number: {result}", self)
            self.layout.addWidget(result_label)

            reset_button = QPushButton("Reset", self)
            reset_button.clicked.connect(self.reset_interface)
            self.layout.addWidget(reset_button)

    def reset_interface(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.power_button.setEnabled(True)  # Re-enable the power button after results are calculated
        self.layout.addWidget(self.power_button)

def main():
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
