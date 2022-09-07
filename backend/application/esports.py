from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Integer, Boolean
from apiflask.validators import OneOf
from flask import current_app as app
from . import ComputerIDIn
from flask_login import login_required
from custom_decorators import permissions_required
from application.models import end_pc_use, set_pc_in_use, reset_pc_statuses, get_db_pc_usages

# Configure Blueprint
esports_bp = APIBlueprint(
    name='esports',
    import_name=__name__,
    url_prefix='/esports'
)


class EsportsIn(ComputerIDIn):
    email = String()


class EsportsOut(Schema):
    id = Integer()
    status = Integer()
    email = String()


class EsportsOutMsg(EsportsOut):
    success = Boolean()
    message = String()


@esports_bp.get('/')
@esports_bp.output(EsportsOut(many=True), description="A list of computer usages, first and last names, student emails, and teams.", status_code=200)
@login_required
@permissions_required(['staff', 'admin'])
def get_usages() -> dict:
    """
    Endpoint that returns a list of all current computer usages.

    Returns:
        dict: A list of computer ids, usage ids,
    """
    # Retrieve all current usages and format
    usages = get_db_pc_usages(esports=True)
    return usages


@esports_bp.post('/')
@esports_bp.input(EsportsIn)
@esports_bp.output(EsportsOutMsg, status_code=200)
@login_required
@permissions_required(['staff', 'admin'])
def set_usage(data: dict) -> dict:
    """
    Endpoint that sets an esports pc into use.

    Args:
        data (ComputerIDIn): The data containing the valid PC id.

    Returns:
        dict: The new usage id of the computer.
    """
    # create a new usage using
    success, results = set_pc_in_use(data['computer_id'], data['email'])
    return {'success': success} | results


@esports_bp.delete('/<int:computer_id>/<int:usage_id>')
@esports_bp.output(EsportsOutMsg, status_code=200)
@login_required
@permissions_required(['staff', 'admin'])
def end_usage(computer_id: int, usage_id: int) -> dict:
    """
    Endpoint that ends the session at the computer with usage id.

    Args:
        computer_id (int): The computer id to end the usage.
        usage_id (int): The usage id to end.

    Returns:
        dict: Whether the session was successfully ended.
    """
    success, results = end_pc_use(usage_id, computer_id, esports=True)
    return {'success': success} | results
