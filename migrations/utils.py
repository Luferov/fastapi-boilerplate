from typing import Any, Union

from alembic.autogenerate.api import AutogenContext
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy_utils.types.json import JSONType
from sqlalchemy_utils.types.uuid import UUIDType  # if alembic is used


def render_item(type_: str, obj: Any, autogen_context: AutogenContext) -> Union[str, bool]:
    '''
    Apply custom rendering for selected items.
    '''

    if type_ == 'type' and isinstance(obj, ChoiceType):
        autogen_context.imports.add('import sqlalchemy_utils')
        autogen_context.imports.add(f'from {obj.choices.__module__} import {obj.choices.__name__}')  # type: ignore
        return f'sqlalchemy_utils.types.ChoiceType({obj.choices.__name__}, impl=sa.{obj.impl.__class__.__name__}())'  # type: ignore

    if type_ == 'type' and isinstance(obj, JSONType):
        autogen_context.imports.add('import sqlalchemy_utils')
        return 'sqlalchemy_utils.types.JSONType()'

    if type_ == 'type' and isinstance(obj, UUIDType):
        autogen_context.imports.add('import sqlalchemy_utils')
        return f'sqlalchemy_utils.types.UUIDType(binary={obj.binary})'

    # Default rendering for other objects
    return False