# AIssistant
Implementation of a AI assistant consisting of STT (Silero - ?) + LLM(ChatGPT - ?) + TTS (Silero)

This is a "just for fun" non-commercial project.

## How to run it?
1. Install used tools: flac

For Mac OS (for example):
```commandline
brew install flac
brew install portaudio
```

2. Install Python 3.10+.

3. Install Poetry:

```commandline
pip3 install poetry
```

4. Install libraries:

```commandline
poetry install
```

5. Run examples:
    
    TTS:
    ```commandline
    poetry run python -m  src.tts_examples
    ```
   
    Additional audio (record and play) adapters:
    ```commandline
    poetry run python -m  src.audio.examples
    ```