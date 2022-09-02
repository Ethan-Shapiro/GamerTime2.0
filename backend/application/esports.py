from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Integer
from apiflask.validators import OneOf
from flask import current_app as app
from . import ComputerIDIn, UsageIn
from flask_login import login_required
from custom_decorators import permissions_required
from application.models import end_pc_use, get_pc_statuses, set_pc_in_use, reset_pc_statuses, get_db_pc_usages

# Configure Blueprint
esports_bp = APIBlueprint(
    name='openrec',
    import_name=__name__,
    url_prefix='/openrec'
)


class EsportsOut(Schema):
    computer_id = Integer()
    usage_id = Integer()
    email = String()


@esports_bp.get('/')
@esports_bp.output(EsportsOut(many=True), description="A list of computer usages, first and last names, student emails, and teams.", status_code=200)
@login_required
@permissions_required(['staff', 'admin', 'openrec'])
def get_usages() -> dict:
    """
    Endpoint that returns a list of all current computer usages.

    Returns:
        dict: A list of computer ids, usage ids,
    """

    return {
        'usageId': 100,
        'startTimestamp': '1234323432'
    }


@esports_bp.post('/')
@esports_bp.input(ComputerIDIn)
@esports_bp.output(EsportsOut, status_code=200)
@login_required
@permissions_required(['staff', 'admin', 'openrec'])
def set_usage(data: ComputerIDIn) -> dict:
    """
    Endpoint that sets an esports pc into use.

    Args:
        data (ComputerIDIn): The data containing the valid PC id.

    Returns:
        dict: The new usage id of the computer.
    """

    return {
        'usageId': 100,
        'startTimestamp': '1234323432'
    }


@esports_bp.delete('/')
@esports_bp.input(UsageIn)
@esports_bp.output(EsportsOut, status_code=200)
@login_required
@permissions_required(['staff', 'admin', 'openrec'])
def end_usage(data: UsageIn) -> dict:
    """
    Endpoint that ends the session at the computer with usage id.

    Args:
        data (UsageIn): The data containing the usage id.

    Returns:
        dict: Whether the usage id was successfully ended.
    """

    return {
        'usageId': 100,
        'startTimestamp': '1234323432'
    }
