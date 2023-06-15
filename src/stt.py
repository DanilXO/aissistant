import json
import os.path

import speech_recognition
from vosk import Model

from src.settings import SETTINGS


class Recognizer:

    def __init__(self):
        self.engine = speech_recognition.Recognizer()
        self.engine.pause_threshold = 0.5
        self.engine.non_speaking_duration = 0.3
        print(SETTINGS.stt_model_path)
        self.engine.vosk_model = Model(
            model_path=SETTINGS.stt_model_path,
            model_name=os.path.basename(SETTINGS.stt_model_path),
            lang=SETTINGS.language
        )

    def recognize(self) -> str:
        with speech_recognition.Microphone(device_index=0) as source:
            audio_data = self.engine.listen(source)
        recognized_result = self.engine.recognize_vosk(audio_data, language=SETTINGS.language)
        try:
            parsed_result = json.loads(recognized_result)
            return parsed_result["text"]
        except (KeyError, ValueError):
            return recognized_result
