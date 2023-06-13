from dataclasses import dataclass, asdict
from enum import Enum
import os
from typing import Any, Dict, Optional, Union
import torch

from src.settings import AllowedLanguages, SETTINGS


class AllowedDevices(Enum):
    CPU = "cpu"
    GPU = "gpu"


class AllowedRUSpeakers(Enum):
    Aidar = "aidar"
    Baya = "baya"
    Kseniya = "kseniya"
    Xenia = "xenia"
    Eugene = "eugene"
    Random = "random"


def get_speaker_by_language(language: AllowedLanguages) -> str:
    if language is AllowedLanguages.RU:
        return AllowedRUSpeakers.Baya.value
    return "en_0"


@dataclass
class SimpleTTSConfig:
    sample_rate: int = 48000
    put_accent: bool = True
    put_yo: bool = True
    symbol_durs: Optional[dict] = None

    def as_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["speaker"] = get_speaker_by_language(SETTINGS.language)
        return result


@dataclass
class SSMLTTSConfig:
    is_ssml: bool = False
    sample_rate: int = 48000
    put_accent: bool = True
    put_yo: bool = True
    symbol_durs: Optional[dict] = None

    def as_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["speaker"] = get_speaker_by_language(SETTINGS.language)
        return result


class SileroTTS:

    def __init__(self, model_file: Union[str, os.PathLike],
                 device_to_launch: AllowedDevices = AllowedDevices.CPU,
                 used_threads_count: int = 4) -> None:

        torch.set_num_threads(used_threads_count)

        self._model_file = model_file
        self._model = torch.package.PackageImporter(
            model_file).load_pickle("tts_models", "model")
        self._model.to(torch.device(device_to_launch.value))

    def synthesize_into_bytes(self,
                              text: str,
                              config: Optional[Union[SimpleTTSConfig, SSMLTTSConfig]] = None) -> bytes:
        if config is None:
            config = SimpleTTSConfig()

        audio = self._model.apply_tts(text, **config.as_dict())
        return bytes((audio * 32767).numpy().astype("int16"))

    def synthesize_into_file(self,
                             text: str,
                             output_file: Union[str, os.PathLike] = "test.wav",
                             config: Optional[Union[SimpleTTSConfig, SSMLTTSConfig]] = None) -> str:

        if config is None:
            config = SimpleTTSConfig()

        return self._model.save_wav(text, **config.as_dict(), audio_path=output_file)
