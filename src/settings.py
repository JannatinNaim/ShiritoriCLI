

class Settings:
    def __init__(
        self,
        initial_word,
        command_prefix
    ):
        self.initial_word = initial_word
        self.command_prefix = command_prefix


settings = Settings(
    initial_word="soup",
    command_prefix="!"
)
