import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QProgressBar
from PyQt5.QtCore import QProcess, QTimer, Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 800)
        

        # Create a layout for the window
        layout = QVBoxLayout(self)

       
        
        
        # Create a Text widget and add it to the layout
        self.output_textbox = QTextEdit(self)
        self.output_textbox.setFontPointSize(12)
        layout.addWidget(self.output_textbox)
        self.setStyleSheet("background-color: black ;color: cyan;")
        
         # Create a progress bar widget and add it to the layout
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange( 0,1000 )
        layout.addWidget(self.progress_bar)
        

        # Create a Button widget and add it to the layout
        self.rfid_scanner = QPushButton('Start', self)
        self.rfid_scanner.clicked.connect(self.run_rfid_scanner)
        layout.addWidget(self.rfid_scanner)
        self.rfid_scanner.setStyleSheet("background-color: #033118; color: #EFF3F3;")

        #create a button for stop scanning
        self.rfid_scanner_stop = QPushButton('Stop Scanning', self)
        self.rfid_scanner_stop.setDisabled(True)
        self.rfid_scanner_stop.clicked.connect(self.stop_rfid_scanner)
        layout.addWidget(self.rfid_scanner_stop)
        self.rfid_scanner_stop.setStyleSheet("background-color: #390F20; color: white;")

       

        # Create a QTimer to update the progress bar
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)

    def run_rfid_scanner(self):
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        self.process.finished.connect(self.handle_finish)
        self.process.start('python', ['ptop.py'])
        self.timer.start(4000)

        self.rfid_scanner.setDisabled(True)
        self.rfid_scanner_stop.setEnabled(True)

    def handle_output(self):
        output = bytes(self.process.readAllStandardOutput()).decode('utf-8')
        self.output_textbox.insertPlainText(output)

    def handle_error(self):
        error = bytes(self.process.readAllStandardError()).decode('utf-8')
        self.output_textbox.insertPlainText(error)

    def handle_finish(self):
        self.timer.stop()
        self.progress_bar.setValue(0)
        self.rfid_scanner.setEnabled(True)
        self.rfid_scanner_stop.setDisabled(True)

    def stop_rfid_scanner(self):
        self.process.terminate()
        self.handle_finish()

    def update_progress_bar(self):
        progress = self.progress_bar.value() + 10
        if progress > self.progress_bar.maximum():
            progress = 0
        self.progress_bar.setValue(progress)

# Create an instance of the application and run it
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
