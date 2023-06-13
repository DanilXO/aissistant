import os
import pathlib
from typing import Union

current_dir = pathlib.Path(__file__).parent.resolve()


def get_resources_path() -> Union[str, os.PathLike]:
    """ Get path to resources folder and create folder if it doesn't exist. """
    current_dir = pathlib.Path(__file__).parent.resolve()
    pathlib.Path(os.path.join(current_dir, 'resources')).mkdir(parents=True, exist_ok=True)
    return os.path.join(current_dir, 'resources')
