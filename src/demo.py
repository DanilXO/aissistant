from random import randint

from src.audio import Player
from src.settings import SETTINGS
from src.stt import Recognizer
from translator import gettext as _
from src.tts import SimpleTTSConfig, SileroTTS


def run_simple_tts_stt_scenario():

    tts = SileroTTS(SETTINGS.tts_model_path)

    tts_config = SimpleTTSConfig(sample_rate=48000)

    is_over = False
    stop_words = (_("exit"), _("finish"), _("let's finish"), _("the end"))
    recognizer = Recognizer()
    exclamations = (_("Great"), _("Super"), _("Nice"), _("Awesome"), _("Fine"))

    with Player() as player:
        data = tts.synthesize_into_bytes(
            text=_("Hello! I am your personal assistant. Let's work? If you want to end, say 'exit'."),
            config=tts_config)
        player.play_data(data, fps=tts_config.sample_rate)

        while not is_over:
            result = recognizer.recognize()

            for stop_word in stop_words:
                if stop_word in result:
                    data = tts.synthesize_into_bytes(
                        text=_("I heard that you want to end our communication. Best wishes!"),
                        config=tts_config)
                    is_over = True
                    player.play_data(data, fps=tts_config.sample_rate)
                    break

            if is_over:
                break

            data = tts.synthesize_into_bytes(
                text="{question}: {result}".format(question=_("Did you say it?"), result=result),
                config=tts_config)

            player.play_data(data, fps=tts_config.sample_rate)

            exclamation = exclamations[randint(0, len(exclamations) - 1)]

            data = tts.synthesize_into_bytes(
                text="{exclamation}! {phrase}".format(exclamation=exclamation,
                                                      phrase=_("Do you want to say me something else?")),
                config=tts_config)

            player.play_data(data, fps=tts_config.sample_rate)


if __name__ == '__main__':
    run_simple_tts_stt_scenario()
