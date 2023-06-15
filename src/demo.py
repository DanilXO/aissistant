from random import randint

from src.audio import Player
from src.settings import SETTINGS
from src.stt import Recognizer
from src.translator import get_text as _
from src.tts import SimpleTTSConfig, SileroTTS


def run_simple_tts_stt_scenario():

    tts = SileroTTS(SETTINGS.tts_model_path)

    tts_config = SimpleTTSConfig(sample_rate=48000)

    is_over = False
    stop_words = (_("выход"), _("закончить"), _("давай заканчивать"), _("конец"))
    recognizer = Recognizer()
    exclamations = (_("Здорово"), _("Супер"), _("Чудненько"), _("Потрясно"), _("Хорошо"), _("Славно"))

    with Player() as player:
        data = tts.synthesize_into_bytes(
            text=_("Привет! Я Ваш личный ассистент. Поработаем? Если хотите закончить, скажите: выход."),
            config=tts_config)
        player.play_data(data, fps=tts_config.sample_rate)

        while not is_over:
            result = recognizer.recognize()

            for stop_word in stop_words:
                if stop_word in result:
                    data = tts.synthesize_into_bytes(
                        text=_("Я услышала, что вы хотите закончить наше общение. Всего хорошего!"),
                        config=tts_config)
                    is_over = True
                    player.play_data(data, fps=tts_config.sample_rate)
                    break

            if is_over:
                break

            data = tts.synthesize_into_bytes(
                text="{}: {}".format(_("Вы сказали?"), result),
                config=tts_config)

            player.play_data(data, fps=tts_config.sample_rate)

            exclamation = exclamations[randint(0, len(exclamations) - 1)]

            data = tts.synthesize_into_bytes(
                text="{}! {}".format(exclamation, _("Скажите еще что-нибудь?")),
                config=tts_config)

            player.play_data(data, fps=tts_config.sample_rate)


if __name__ == '__main__':
    run_simple_tts_stt_scenario()
