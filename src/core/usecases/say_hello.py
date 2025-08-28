class SayHelloUseCase:
    def __init__(self, hello_message: str):
        self._hello_message = hello_message

    def execute(self) -> str:
        return self._hello_message