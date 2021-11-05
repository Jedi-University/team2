class ConsoleProgressBar:

    __PROGRESS_CHAR = "▓"
    __EMPTY_CHAR = "░"
    __MAX_VALUE = 100

    def __init__(self, description: str, current_progress: int = 0) -> None:
        self.current_progress = current_progress
        self.description = description
        print(description)

    def update_progress(self, element: float, max_elements: float) -> None:
        delta_for_progress = int(100 * element / max_elements) - self.current_progress
        if delta_for_progress > 0:
            self.current_progress += delta_for_progress
            self._print(self.current_progress)

    def reset(self):
        self.__init__(self.description)

    def _print(self, value) -> None:
        line = self.__PROGRESS_CHAR * value + self.__EMPTY_CHAR * (self.__MAX_VALUE - value)
        print("\r" + line, end="")
