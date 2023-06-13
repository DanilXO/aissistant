import os.path

import speech_recognition
from vosk import Model

from src.utils import get_resources_path


class Recognizer:
    vosk_model_name = "stt_vosk"
    lang = "ru"

    def __init__(self):
        self.engine = speech_recognition.Recognizer()
        self.engine.pause_threshold = 0.5
        self.engine.non_speaking_duration = 0.3
        self.engine.vosk_model = Model(
            model_path=os.path.join(get_resources_path(), self.vosk_model_name),
            model_name=self.vosk_model_name,
            lang=self.lang
        )

    def recognize(self) -> str:
        with speech_recognition.Microphone(device_index=0) as source:
            audio_data = self.engine.listen(source)

        return self.engine.recognize_vosk(audio_data, language=self.lang)
