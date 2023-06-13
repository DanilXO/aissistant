from random import randint

from src.audio import Player
from src.settings import SETTINGS
from src.stt import Recognizer
from src.tts import SimpleTTSConfig, SileroTTS


def run_simple_tts_stt_scenario():

    tts = SileroTTS(SETTINGS.tts_model_path)

    tts_config = SimpleTTSConfig(sample_rate=48000)

    is_over = False
    stop_words = ("выход", "закончить", "давай заканчивать", "конец")
    recognizer = Recognizer()
    exclamations = ("Здорово", "Супер", "Чудненько", "Потрясно", "Хорошо", "Славно")

    with Player() as player:
        data = tts.synthesize_into_bytes(
            text="Привет! Я Ваш личный ассистент. Поработаем? Если хотите закончить, скажите: выход.",
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
