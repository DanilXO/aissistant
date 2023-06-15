import csv

from src.settings import AllowedLanguages, SETTINGS


class TranslatorError(Exception):
    pass


class NoFoundBaseLanguagePhrase(TranslatorError):
    pass


class InvalidTranslationRow(TranslatorError):
    pass


class Translator:
    delimiter = "~"
    base_language = AllowedLanguages.RU

    def __init__(self, translation_path: str):

        self._translation_path = translation_path
        self._phrase_maps = {}

        self._load_phrase_map()

    def _load_phrase_map(self):
        with open(self._translation_path, encoding="utf-8") as fp:
            phrases_reader = csv.DictReader(fp, delimiter=self.delimiter)
            for row in phrases_reader:
                get_method = getattr(row, "get", None)

                if get_method is None:
                    raise InvalidTranslationRow

                key = get_method(self.base_language.value, None)
                if key is None:
                    raise NoFoundBaseLanguagePhrase
                self._phrase_maps[key] = row

    def get_text(self, phrase: str) -> str:
        phrase_map = self._phrase_maps.get(phrase, {})
        return phrase_map.get(SETTINGS.language.value, "")


TRANSLATOR = Translator(SETTINGS.translation_path)


def get_text(phrase: str) -> str:
    return TRANSLATOR.get_text(phrase)
