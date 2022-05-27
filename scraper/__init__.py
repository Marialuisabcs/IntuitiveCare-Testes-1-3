import shutil
from pathlib import Path

import colorama

colorama.init()
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN


def zip_file(output_file_name: str, path: str):
    """
    Compress files and folders
    :param output_file_name: Path with the desired name of the new zipped file
    :param path: Path relative to the root path of the file to be zipped
    """
    zip_file_name = shutil.make_archive(base_name=output_file_name, base_dir=path, format='zip')
    print(f'{GREEN}[!]{zip_file_name} zipped')
