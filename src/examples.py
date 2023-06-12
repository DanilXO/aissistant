import os
import pathlib
from random import randint

from src.audio import Player
from src.stt import Recognizer
from src.tts import SimpleTTSConfig, SileroTTS, AllowedSpeakers, download_silero_tts_model


def run_simple_tts_stt_scenario():
    current_dir = pathlib.Path(__file__).parent.resolve()

    pathlib.Path(os.path.join(current_dir, 'resources')).mkdir(parents=True, exist_ok=True)

    model_file = os.path.join(current_dir, 'resources', 'tts_sliero_v3.pt')
    download_silero_tts_model(model_file)

    tts = SileroTTS(model_file)
    tts_config = SimpleTTSConfig(
        speaker=AllowedSpeakers.Baya,
        sample_rate=48000,
    )

    is_over = False
    stop_words = ("выход", "закончить", "давай заканчивать", "конец")
    recognizer = Recognizer()
    exclamations = ("Здорово", "Супер", "Чудненько", "Потрясно", "Хорошо", "Славно")

    with Player() as player:
        data = tts.synthesize_into_bytes(
            text="Привет! Я Ваш искусственный ассистент. Поработаем? Если хотите закончить, скажите: выход.",
            config=tts_config)
        player.play_data(data, fps=tts_config.sample_rate)

        while not is_over:
            result = recognizer.recognize()

            for stop_word in stop_words:
                if stop_word in result:
                    data = tts.synthesize_into_bytes(
                        text=f"Я услышала, что вы хотите закончить наше общение. Всего хорошего!",
                        config=tts_config)
                    is_over = True
                    player.play_data(data, fps=tts_config.sample_rate)
                    break

            if is_over:
                break

            data = tts.synthesize_into_bytes(
                text=f"Вы сказали: {result}?",
                config=tts_config)
            player.play_data(data, fps=tts_config.sample_rate)

            exclamation = exclamations[randint(0, len(exclamations) - 1)]

            data = tts.synthesize_into_bytes(
                text=f"{exclamation}! Скажите еще что-нибудь?",
                config=tts_config)

            player.play_data(data, fps=tts_config.sample_rate)


if __name__ == '__main__':
    run_simple_tts_stt_scenario()
