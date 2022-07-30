from settings import settings

command_prefix = settings.command_prefix


class Command:
    def __init__(self, string: str):
        self.is_command: bool = string.startswith(command_prefix)
        self.action: str = ""

        if self.is_command:
            self.action: str = string[string.index(command_prefix) + 1:]
