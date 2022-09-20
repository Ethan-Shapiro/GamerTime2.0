from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Integer, Boolean
from flask import current_app as app
from . import ComputerIDIn
from custom_decorators import perms_required
from flask_jwt_extended import jwt_required
from application.models import end_pc_use, set_pc_in_use, get_queue, add_to_queue, remove_from_queue, get_db_pc_usages, get_computer_availability
from flask_cors import CORS

# Configure Blueprint
openrec_bp = APIBlueprint(
    name='openrec',
    import_name=__name__,
    url_prefix='/api/openrec'
)


class OpenRecOut(Schema):
    id = Integer()
    status = Integer()
    start_timestamp = String()


class OpenRecOutMsg(OpenRecOut):
    success = Boolean()
    message = String()


class QueueIn(Schema):
    first_name = String()
    last_name = String()


class QueueOut(Schema):
    id = Integer()
    name = String()


class QueueOutSuccess(QueueOut):
    success = Boolean()


@openrec_bp.get('/')
@openrec_bp.output(OpenRecOut(many=True), description="A list of computer usages and timestamps.", status_code=200)
# @login_required
# @permissions_required(['staff', 'admin', 'openrec'])
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
@openrec_bp.output(OpenRecOutMsg, status_code=200)
@jwt_required()
@perms_required(['admin', 'openrec'])
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


@openrec_bp.post('/queue')
@openrec_bp.input(QueueIn)
@openrec_bp.output(QueueOutSuccess)
@jwt_required()
@perms_required(['admin', 'openrec'])
def queue_in(data) -> dict:
    """
    Endpoint that sets an openrec pc into use.

    Args:
        data (OpenRecIn): The data containing the valid PC id.

    Returns:
        dict: The new usage id and start timestamp (if successful).
    """
    # create a new usage using
    success, queue_data = add_to_queue(data['first_name'], data['last_name'])
    return {'success': success} | queue_data


@openrec_bp.delete('/queue/<int:queue_id>')
@openrec_bp.output(QueueOutSuccess)
@jwt_required()
@perms_required(['admin', 'openrec'])
def queue_out(queue_id: int) -> dict:
    """
    Endpoint that sets an openrec pc into use.

    Args:
        data (OpenRecIn): The data containing the valid PC id.

    Returns:
        dict: The new usage id and start timestamp (if successful).
    """
    # create a new usage using
    success = remove_from_queue(queue_id)
    return {'success': success}


@openrec_bp.get('/queue')
@openrec_bp.output(QueueOut(many=True))
@jwt_required()
@perms_required(['admin', 'openrec'])
def get_current_queue():
    return get_queue()


@openrec_bp.get('/availability')
@jwt_required()
@perms_required(['admin', 'openrec'])
def get_availability() -> bool:
    availability = get_computer_availability()
    return availability


@openrec_bp.delete('/<int:computer_id>/<int:usage_id>')
@openrec_bp.output(OpenRecOutMsg, status_code=200)
@jwt_required()
@perms_required(['admin', 'openrec'])
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
