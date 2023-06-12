import os
import pathlib

from src.audio import Player
from src.tts import SimpleTTSConfig, TTSAdapter, AllowedSpeakers, download_silero_tts_model


def generate_tts_and_play():
    current_dir = pathlib.Path(__file__).parent.resolve()

    pathlib.Path(os.path.join(current_dir, 'resources')).mkdir(parents=True, exist_ok=True)

    model_file = os.path.join(current_dir, 'resources', 'tts_sliero_v3.pt')
    download_silero_tts_model(model_file)

    tts = TTSAdapter(model_file)
    tts_config = SimpleTTSConfig(
        speaker=AllowedSpeakers.Baya,
        sample_rate=48000,
    )
    data = tts.recognize_to_bytes(
        text='Карл у Клары украл кораллы, а Клара у Карла кларнет.', config=tts_config)

    with Player() as player:
        player.play_data(data, fps=tts_config.sample_rate)


if __name__ == '__main__':
    generate_tts_and_play()
