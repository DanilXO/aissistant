import os
import pathlib
from enum import Enum
from typing import Optional, Dict, Any, Union

from pydantic import BaseSettings, Field, root_validator
from pydantic.types import Path

ComputedPath = Optional[Union[str, Path, os.PathLike]]


class AllowedLanguages(Enum):
    EN = "en_US"
    RU = "ru_RU"


class Settings(BaseSettings):
    language: AllowedLanguages = Field(env="language", default=AllowedLanguages.EN)
    resources_dir_name: str = Field(env="resources_dir_name", default="resources")

    language_models_map: Dict[str, Dict[AllowedLanguages, str]] = {
        "tts": {
            AllowedLanguages.EN: "silero_v3_en.pt",
            AllowedLanguages.RU: "sliero_v3_ru.pt",
        },
        "stt": {
            AllowedLanguages.EN: "vosk-model-small-en-us-0.15",
            AllowedLanguages.RU: "vosk-model-small-ru-0.22",
        },
    }

    source_dir_path: ComputedPath
    resources_dir_path: ComputedPath
    tts_model_path: ComputedPath
    stt_model_path: ComputedPath
    translation_path: ComputedPath
    locales_path: ComputedPath

    @root_validator
    def _init_computed_settings(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        source_dir_path = ""
        resources_dir_path = ""
        language: AllowedLanguages = values.get("language", AllowedLanguages.RU)
        language_models_map = values.get("language_models_map", {})

        try:
            if values.get("source_dir_path", None) is None:
                source_dir_path = pathlib.Path(__file__).parent.parent.resolve()
                values["source_dir_path"] = source_dir_path

            if values.get("resources_dir_path", None) is None:
                resources_dir_path = os.path.join(source_dir_path, values["resources_dir_name"])
                values["resources_dir_path"] = resources_dir_path

            if values.get("translation_path", None) is None:
                values["translation_path"] = os.path.join(resources_dir_path, "translation.csv")

            if values.get("locales_path", None) is None:
                values["locales_path"] = os.path.join(source_dir_path, "locales", language.value, "LC_MESSAGES",
                                                      "messages.mo")

            values.update(cls._load_language_models_configs(language, language_models_map, resources_dir_path))

        except KeyError as err:
            raise ValueError(f"{err.args[0]} is required setting param.")

        return values

    @classmethod
    def _load_language_models_configs(
            cls, language: AllowedLanguages,
            language_models_map: Dict[str, Dict[AllowedLanguages, str]],
            resources_dir_path: ComputedPath) -> Dict[str, Any]:
        language_models_configs = {}

        tts_model_name = language_models_map.get("tts", {}).get(language)
        if tts_model_name is None:
            raise ValueError(f"Invalid 'language_models_map' param. "
                             f"It doesn't have '{language.value.upper()}' tts model name.")

        stt_model_name = language_models_map.get("stt", {}).get(language)
        if stt_model_name is None:
            raise ValueError(f"Invalid 'language_models_map' param. "
                             f"It doesn't have '{language.value.upper()}' stt model name.")

        language_models_configs["tts_model_path"] = os.path.join(resources_dir_path, "tts", tts_model_name)
        language_models_configs["stt_model_path"] = os.path.join(resources_dir_path, "stt", stt_model_name)

        return language_models_configs


SETTINGS = Settings()
