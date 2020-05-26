# System imports
import time
import logging

# 3rd party projects
import flask
import pymongo

# Package imports
from . import db

app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """ Simple healthcheck endpoint. """
    return flask.jsonify({"ok": time.time()})


@app.route("/mongo/version", methods=["GET"])
def mongo_version():
    """ Bootstrapping endpoint to ensure we have a working API. """
    return flask.jsonify({"version": pymongo.__version__})


@app.route("/create/<obj_type>/<_id>", methods=["POST"])
def create(obj_type, _id):
    """
    Endpoint for creating a generic object.

    Args:
        obj_type: Object type, which should be a collection name
        _id: Unique ID for this object

    """
    log = logging.getLogger("quickpickup.create")

    # Get the JSON body which will be our object with its attributes
    obj = flask.request.get_json()

    # Make sure we actually got an object
    if not obj:
        log.error(f"Bad request: obj = {obj}")
        flask.abort(400)

    # Forcefully assign the given ID
    obj["_id"] = _id

    # TODO: Validation to disallow bad object types
    # Get the object type collection
    coll = db.collection(obj_type)
    try:
        result = coll.insert_one(obj)
    except pymongo.errors.OperationFailure as err:
        log.exception(err)
        flask.abort(409)

    return {"_id": result.inserted_id}
