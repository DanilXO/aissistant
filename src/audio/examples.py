import os
import pathlib

from src.audio import Recorder, Player


def record_into_file_and_play() -> None:
    """ Record audio from microphone and play it with save in file"""
    recorder = Recorder()
    parent_dir = pathlib.Path(__file__).parent.parent.resolve()
    file_path = os.path.join(parent_dir, 'resources', 'output.wav')

    with Recorder() as recorder:
        recorder.record_and_save(
            seconds=5, output_path=file_path)

    with Player() as player:
        player.play_file(file_path)


def record_into_bytes_and_play() -> None:
    """ Record audio from microphone and play it without save """

    with Recorder() as recorder:
        data = recorder.record(seconds=5)

    with Player() as player:
        player.play_data(data, format=recorder.config.sample_format,
                         channels=recorder.config.channels, fps=recorder.config.fps)


if __name__ == '__main__':
    record_into_bytes_and_play()
