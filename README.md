# AIssistant
Implementation of a AI assistant consisting of STT (Silero - ?) + LLM(ChatGPT - ?) + TTS (Silero)

This is a "just for fun" non-commercial project.

## How to run it?

1. Install Python 3.10+.

2. Install Poetry

```commandline
pip3 install poetry
```

3. Run examples

Audio record and play adapters:
```commandline
poetry run python -m  src.audio.examples
```

TTS:
```commandline
poetry run python -m  src.tts_examples
```