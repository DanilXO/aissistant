import speech_recognition


class Recognizer:
    def __init__(self):
        self.engine = speech_recognition.Recognizer()

    def recognize(self) -> str:
        with speech_recognition.Microphone(device_index=0) as source:
            audio_data = self.engine.listen(source)
        return self.engine.recognize_google(audio_data, language="ru-RU")


if __name__ == '__main__':
    recognizer = Recognizer()
    result = recognizer.recognize()
    print(result)

