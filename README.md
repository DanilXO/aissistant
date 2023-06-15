# AIssistant
Implementation of a AI assistant consisting of STT (Vosk) + LLM(ChatGPT - ?) + TTS (Silero)

This is a "just for fun" non-commercial project.

## How to run it?
1. Clone this repository
2. Download models from [here](https://drive.google.com/file/d/17a0qRIIWUd8ucfwp0ol2meCiwnwdfjgp/view?usp=sharing) 
and unzip it into repository.
3. Install used tools: portaudio, flac

For Mac OS (for example):
```commandline
brew install flac
brew install portaudio
```

4. Install Python 3.10+.

5. Install Poetry:

```commandline
pip3 install poetry
```

6. Install libraries:

```commandline
poetry install
```

7. Compile locales translations:

```commandline
pybabel compile -d locales
```

8. Set 'LANGUAGE' environment variable: 'ru_RU' or 'en_US' (en_US by default)

9. Run demo:
```commandline
   poetry run python -m src.demo
```
