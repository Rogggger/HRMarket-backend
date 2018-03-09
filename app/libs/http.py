from flask import Response
import jsonpickle
from app.libs.errorhandler import compose_error


def jsonify(raw=None, status_code=200):
    resp = Response(jsonpickle.encode(raw), mimetype='application/json')
    resp.status_code = status_code
    return resp


def error_jsonify(error_code, specifiy_error="", status_code=400):
    error_resp = compose_error(specifiy_error, error_code)
    return jsonify(error_resp, status_code)
