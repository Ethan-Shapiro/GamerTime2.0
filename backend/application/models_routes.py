from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Integer, Boolean
from apiflask.validators import Length
from flask import current_app as app
from custom_decorators import perms_required
from application.models import create_player, recreate_computer_statuses, reset_computer_statuses_table

# Configure Blueprint
models_bp = APIBlueprint(
    name='models',
    import_name=__name__,
    url_prefix='/api/models'
)


class PlayerIn(Schema):
    first_name = String(validate=[Length(2, 50)])
    last_name = String(validate=[Length(2, 50)])
    email = String()
    role = String(validate=[Length(2, 7)])
    team = String(validate=[Length(2, 5)])


class ModelRoutesOut(Schema):
    success = Boolean()


@models_bp.get('/create_computer_statuses')
@perms_required(['admin'])
def create_computer_statuses() -> bool:
    success = recreate_computer_statuses()
    return {'success': success}


@models_bp.get('/reset_computer_statuses')
@perms_required(['admin'])
def reset_computer_statuses() -> bool:
    success = reset_computer_statuses_table()
    return {'success': success}


@models_bp.post('/add_player')
@models_bp.input(PlayerIn)
@models_bp.output(ModelRoutesOut)
@perms_required(['admin'])
def add_player(data: dict) -> dict:
    """
    Attempts to create a new player in the database with the given attributes.

    Args:
        data (dict): The attributes of the player

    Returns:
        dict: A single key whether the request was successful.
    """
    success, player = create_player(data)
    return {'success': success}
