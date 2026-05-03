SUPPORTED_INPUT_TYPES = {"image"}


class UnsupportedInputTypeError(Exception):
    def __init__(self, input_type: str):
        self.input_type = input_type
        super().__init__(f"Unsupported input type: {input_type}")


def validate_input_type(input_type: str) -> None:
    if input_type not in SUPPORTED_INPUT_TYPES:
        raise UnsupportedInputTypeError(input_type)
