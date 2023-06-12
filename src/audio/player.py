from contextlib import closing
import os
from typing import Union
import pyaudio
import wave

from src.audio.common import PyAudioManager


class Player(PyAudioManager):

    def play_file(self, file_path: Union[str, os.PathLike], chunk_size: int = 1024):
        with closing(wave.open(file_path, 'rb')) as wf:
            data = wf.readframes(chunk_size)
            with closing(self._p.open(
                    format=self._p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(), rate=wf.getframerate(), output=True
            )) as stream:
                while data != b'':
                    stream.write(data)
                    data = wf.readframes(chunk_size)

    def play_data(self, data: bytes, format: int = pyaudio.paInt16, channels: int = 1,
                  fps: int = 8000) -> None:
        with closing(self._p.open(
                format=format, channels=channels, rate=fps, output=True
        )) as stream:
            stream.write(data)
