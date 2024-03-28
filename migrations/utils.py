import sqlalchemy_utils


def render_item(type_, obj, autogen_context):
    """
    Apply custom rendering for selected items.
    """

    if type_ == 'type' and isinstance(obj, sqlalchemy_utils.types.ChoiceType):
        autogen_context.imports.add('import sqlalchemy_utils')
        autogen_context.imports.add(f'from {obj.choices.__module__} import {obj.choices.__name__}')
        return f'sqlalchemy_utils.types.ChoiceType({obj.choices.__name__}, impl=sa.{obj.impl.__class__.__name__}())'

    if type_ == 'type' and isinstance(obj, sqlalchemy_utils.types.JSONType):
        autogen_context.imports.add('import sqlalchemy_utils')
        return 'sqlalchemy_utils.types.JSONType()'

    # Default rendering for other objects
    return False
