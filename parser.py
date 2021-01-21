from enum import Enum

class Command(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

class Parser:
    def __init__(self, file_name: str):
        self.file_name: str = file_name
        self.current_line: int = 0
        self.current_command: str = None
        self._command_type: Command = None
        self.address = 0

        try:
            with open(file_name, "r") as data:
                self.data = data.readlines()
        except FileNotFoundError:
            exit(f"File {file_name} not found.")

    def has_more_commands(self) -> bool:
        if self.current_line >= len(self.data):
            return False
        
        return True

    def advance(self) -> None:
        raw_data = self.data[self.current_line]
        self.current_command = raw_data.split("//")[0].strip()
        self.current_line += 1

        if len(self.current_command) == 0:
            self._command_type = None
            return

        if self.current_command[0] == "@":
            self._command_type = Command.A_COMMAND
            self.address += 1
        elif self.current_command[0] == "(" and self.current_command[-1] == ")":
            self._command_type = Command.L_COMMAND
        elif len(self.current_command) == 0 or self.current_command[0:2] == "//":
            self._command_type = None
        else:
            self._command_type = Command.C_COMMAND
            self.address += 1
    
    def command_type(self) -> Command:
        return self._command_type
    
    def symbol(self) -> str:
        if self._command_type == Command.A_COMMAND:
            return self.current_command[1:]
        elif self._command_type == Command.L_COMMAND:
            command_len = len(self.current_command)
            return self.current_command[1: command_len - 1]
        else:
            exit("symbol function only can be called in A_COMMAND or L_COMMAND.")
    
    def dest(self) -> str:
        if self._command_type != Command.C_COMMAND:
            exit("dest function only can be called in C_COMMAND")

        if self.current_command.find("=") == -1:
            return ""
        
        return self.current_command.split("=")[0]

    def comp(self) -> str:
        if self._command_type != Command.C_COMMAND:
            exit("comp function only can be called in C_COMMAND")

        if self.current_command.find("=") == -1:
            return self.current_command.split(";")[0]

        return self.current_command.split(";")[0].split("=")[1]
        
    
    def jump(self) -> str:
        if self._command_type != Command.C_COMMAND:
            exit("jump function only can be called in C_COMMAND")
        
        if self.current_command.find(";") == -1:
            return None
        
        return self.current_command.split(";")[1]

    def reset(self) -> None:
        self.current_line: int = 0
        self.current_command: str = None
        self._command_type: Command = None
        self.address = 0
