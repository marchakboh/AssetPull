import subprocess
from PySide6.QtCore import QThread, Signal
import ETools

class ProcessRunner(QThread):
    log_signal = Signal(str)

    entries = []

    def set_entries(self, entries_array):
        self.entries = entries_array

    def run(self):
        for item_data in self.entries:
            
            file_url = item_data[ETools.Key_Column4]
            download_command = ["C:/Users/admin/Documents/GitHub/ExternalsTool/Tools/megatools/megatools.exe", "dl", "--path", ETools.ETools.ConfigFolder, file_url]

            download_process = subprocess.Popen(
                download_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            for line in download_process.stdout:
                self.log_signal.emit(line.strip())

            download_process.wait()

            dest_folder = item_data[ETools.Key_Column2]



