from os import stat
import time
from apiflask import APIBlueprint
from flask import Blueprint, render_template, request
from flask import current_app as app
from flask_login import login_required
from custom_decorators import permissions_required
from application.models import end_pc_use, get_pc_statuses, set_pc_in_use, reset_pc_statuses, get_db_pc_usages

# Configure Blueprint
openrec = APIBlueprint(
    name='openrec', import_name=__name__
)


@openrec.route('/openrec', methods=['GET'])
@login_required
@permissions_required(['staff', 'admin', 'openrec'])
def openrec_page():
    """OpenRec Page."""
    new_statuses = get_db_pc_usages(esports=False)
    statuses = get_pc_statuses()
    print(new_statuses)
    return render_template('openrec.html', computer_statuses=statuses, computer_info=new_statuses)


@openrec.route('/openrec/users', methods=['POST', 'DELETE'])
@login_required
@permissions_required(['staff', 'admin', 'openrec'])
def openrec_usages():
    """A route for any openrec changes to the usages of the computers"""
    if request.method == 'POST':
        computer_id = request.json['computer_id']
        return set_pc_in_use(computer_id)

    if request.method == 'DELETE':
        print(request.json)
        usage_id = request.json['usage_id']
        computer_id = request.json['computer_id']
        return end_pc_use(usage_id, computer_id)

    return "Something failed with the request."


@openrec.route('/openrec/redis_reset', methods=['GET'])
@login_required
@permissions_required('admin')
def redis_reset():
    if request.method == 'GET':
        reset_pc_statuses()
