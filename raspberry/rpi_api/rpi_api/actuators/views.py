from flask import request, jsonify, Blueprint, current_app as app


blueprint = Blueprint('actuators', __name__, url_prefix='/actuators')


@blueprint.route('/startWatering', methods=['GET'])
def start_watering():

    ret = {
        'something_key': 'something',
    }
    return jsonify(ret), 200
