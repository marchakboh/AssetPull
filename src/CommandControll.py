import ETools
from CommandRunner import CommandRunner

class CommandControll:

    def __init__(self):
        self.commands = {}
        self.current_command = ""
        self.runner = CommandRunner()
    
    def run_process(self, array_data):
        self.commands.clear()

        for item in array_data:
            command = []
            if item[ETools.Key_ColumnType] == ETools.SupportedTypes.Mega.name:
                command = ["C:\\Users\\admin\\Documents\\GitHub\\ExternalsTool\\Tools\\megatools\\megatools.exe", "dl", "--path", ETools.ETools.get_temp_folder(), item[ETools.Key_ColumnURL]]
            self.commands[item[ETools.Key_ColumnName]] = command
        print(self.commands)
        if len(self.commands.items()) > 0:
            self.current_command = list(self.commands.keys())[0]
            self.runner.run_command(self.commands[self.current_command], self.on_log, self.on_end_process)
    
    def on_log(self, log):
        print(log)

    def on_end_process(self):
        print("ended")
        self.commands.pop(self.current_command)

        if len(self.commands.items()) > 0:
            self.current_command = list(self.commands.keys())[0]
            self.runner.run_command(self.commands[self.current_command], self.on_log, self.on_end_process)
