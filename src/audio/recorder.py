import os
from dataclasses import dataclass
from typing import Optional, Union
import pyaudio
import wave

from src.audio.common import PyAudioManager, log


@dataclass
class RecordConfig:
    chunk: int = 1024  # Record in chunks of 1024 samples
    sample_format: int = pyaudio.paInt16  # 16 bits per sample
    channels: int = 1
    fps: int = 44100  # Record at 44100 samples per second


class Recorder(PyAudioManager):

    def __init__(self, config: Optional[RecordConfig] = None) -> None:
        super().__init__()
        if config is None:
            config = RecordConfig()
        self.config = config

    def record_and_save(self, seconds: int, output_path: Union[str, os.PathLike]) -> None:
        frames = self.record(seconds)
        self.save(frames, output_path)

    def record(self, seconds: int) -> bytes:
        log.info('Start recording.')
        port_audio = pyaudio.PyAudio()
        frames = []
        stream = port_audio.open(format=self.config.sample_format,
                                 channels=self.config.channels,
                                 rate=self.config.fps,
                                 frames_per_buffer=self.config.chunk,
                                 input=True)

        for _ in range(0, int(self.config.fps / self.config.chunk * seconds)):
            frame = stream.read(self.config.chunk)
            frames.append(frame)
        log.info('Recording finished.')
        return b''.join(frames)

    def save(self, data: bytes, path: Union[str, os.PathLike]) -> None:
        port_audio = pyaudio.PyAudio()
        out = wave.open(path, 'wb')
        try:
            out.setnchannels(self.config.channels)
            out.setsampwidth(port_audio.get_sample_size(
                self.config.sample_format))
            out.setframerate(self.config.fps)
            out.writeframes(data)
        finally:
            out.close()
            port_audio.terminate()
        log.info(f'File saved on: {path}.')
