from flask import send_from_directory, Blueprint
from flask import current_app as app
import os

react_bp = Blueprint(name='react', import_name=__name__)


@react_bp.get('/', defaults={'path': ''})
@react_bp.get('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
