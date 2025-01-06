import logging
import logging.config
from os.path import exists, join

import yaml

from src.settings import settings

__all__ = ('set_logging',)


def set_logging() -> None:
    """
    Модель настройки логирования.
    """

    files = ['.logging.dev.yaml', '.logging.yaml']
    for file in files:
        ls_file = join(settings.base_dir, file)
        if exists(ls_file):
            with open(ls_file, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            break
    else:
        print(f'Отсутствуют конфигурационные файлы: {", ".join(files)}')
        exit(0)
