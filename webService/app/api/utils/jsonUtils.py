import json
from bottle import response
from api.utils.logManager import LogManager


def json_error_return(message="Unknown Error"):

    response.headers["Content-Type"] = "application/json"
    LogManager.error_log("jsonUtils -- " + str(message))

    return json.dumps({"status": "ERROR", "message": str(message)})


def json_success_return(value=None):
    if not value:
        value = {}

    response.headers["Content-Type"] = "application/json"
    return json.dumps({"status": "SUCCESS", "data": value})
