import importlib
import json
import os
from collections import defaultdict
from pathlib import Path

import sqlalchemy as sa

from src.core.db import AsyncSessionFactory
from src.settings import settings
from src.tools.app import app
from src.tools.utils import typer_async


def import_from_string(import_str: str):
    package_name, model_name = import_str.rsplit('.', maxsplit=1)
    package = importlib.import_module(package_name)
    return getattr(package, model_name), model_name


@app.command(
    name='loaddata',
    help='uv run python manage.py',
)
@typer_async
async def loaddata():
    seed_dir = Path(settings.base_dir) / 'seed'
    seq_counter = defaultdict(int)
    for seed_file in os.listdir(seed_dir):
        seed_file_path = seed_dir / seed_file

        with open(seed_file_path) as f:
            items = json.load(f)

        async with AsyncSessionFactory() as s, s.begin():
            for item in items:
                model, model_name = import_from_string(item['model'])
                seq_counter[model_name] += 1
                await s.execute(sa.insert(model).values({'id': item['id'], **item['fields']}))

    async with AsyncSessionFactory() as s, s.begin():
        for model, seq_i in seq_counter.items():
            await s.execute(sa.text('ALTER SEQUENCE {} RESTART WITH {};'.format(f'{model}_id_seq', seq_i + 1)))
