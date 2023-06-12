from logging import getLogger
import pyaudio


class PyAudioManager:
    def __init__(self) -> None:
        self._p = pyaudio.PyAudio()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.terminate()

    def terminate(self):
        self._p.terminate()


log = getLogger("audio")
