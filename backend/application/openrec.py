from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Integer, Boolean
from flask import current_app as app
from . import ComputerIDIn
from flask_login import login_required
from custom_decorators import permissions_required
from application.models import end_pc_use, set_pc_in_use, reset_pc_statuses, get_db_pc_usages

# Configure Blueprint
openrec_bp = APIBlueprint(
    name='openrec',
    import_name=__name__,
    url_prefix='/openrec'
)


class OpenRecOut(Schema):
    id = Integer()
    status = Integer()
    start_timestamp_seconds = String()


class OpenRecOutMsg(OpenRecOut):
    success = Boolean()
    message = String()


@openrec_bp.get('/')
@openrec_bp.output(OpenRecOut(many=True), description="A list of computer usages and timestamps.", status_code=200)
@login_required
@permissions_required(['staff', 'admin', 'openrec'])
def get_usages() -> dict:
    """
    Endpoint that returns a list of all current computer usages.

    Args:
        data (OpenRecIn): The data containing the valid PC id.

    Returns:
        dict: The new usage id and start timestamp (if successful).
    """
    # Retrieve all current usages and format
    usages = get_db_pc_usages(esports=False)
    return usages


@openrec_bp.post('/')
@openrec_bp.input(ComputerIDIn)
@openrec_bp.output(OpenRecOut, status_code=200)
@login_required
@permissions_required(['staff', 'admin', 'openrec'])
def set_usage(data: ComputerIDIn) -> dict:
    """
    Endpoint that sets an openrec pc into use.

    Args:
        data (OpenRecIn): The data containing the valid PC id.

    Returns:
        dict: The new usage id and start timestamp (if successful).
    """
    # create a new usage using
    success, results = set_pc_in_use(data['computer_id'])
    return {'success': success} | results


@openrec_bp.delete('/<int:computer_id>/<int:usage_id>')
@openrec_bp.output(OpenRecOut, status_code=200)
@login_required
@permissions_required(['staff', 'admin', 'openrec'])
def end_usage(computer_id: int, usage_id: int) -> dict:
    """
    Endpoint that ends a currently in session computer usage.

    Args:
        data (OpenRecIn): The data containing the valid PC id.

    Returns:
        dict: The new usage id and start timestamp (if successful).
    """
    success, results = end_pc_use(usage_id, computer_id, esports=False)
    return {'success': success} | results
