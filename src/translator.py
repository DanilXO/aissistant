from babel.support import Translations

from src.settings import SETTINGS


def gettext(msg: str) -> str:
    with open(SETTINGS.locales_path, "rb") as fp:
        return Translations(fp=fp, domain=SETTINGS.language).gettext(msg)
