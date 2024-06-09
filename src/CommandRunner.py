import subprocess
import threading

class CommandRunner:
    
    def __init__(self):
        self.thread = None

    def run_command(self, command, log_callback, end_callback):
        
        def target():
            print(command)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in process.stdout:
                log_callback(line)
            #process.stdout.close()
            process.wait()
            end_callback()

        self.thread = threading.Thread(target=target)
        self.thread.start()
