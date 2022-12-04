from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from lib import optimus, req_factory

app = Flask(__name__)
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["30 per hour", "15 per minute"]
)

# TESTROUTES
@app.route("/")
@limiter.limit("1 per second")
# Hello World
def hello_world():
    print("hello world")
    return jsonify({"message": "Hello World"})


# PING
@app.route("/ping")
@limiter.limit("1 per second")
def ping():
    return jsonify("pong")


# endpoint to flatten json
@app.route("/flatten", methods=["POST"])
def flatten():
    print("Flatten request received")
    data = request.get_json()

    return jsonify(optimus.flatten_json(data)["out"])


# endpoint to find all fields in json
@app.route("/fields", methods=["POST"])
def fields():
    print(f"Fields request received  {get_remote_address()}")
    data = request.get_json()
    # flatten json
    fields = list(set(optimus.flatten_json(data)["out"].keys()))
    arrays = optimus.flatten_json(data)["arrays"]

    return jsonify({"fields": fields, "arrays": arrays})


# # endpoint to find depth of json
# @app.route("/depth", methods=["POST"])
# def depth():
#     print("Depth request received")
#     data = request.get_json()
#     # flatten json
#     depth = optimus.flatten_json(data)["depth"]
#     # get all fields witout duplicates
#     return jsonify({"depth": depth})

# endpoint to make request
@app.route("/req", methods=["POST"])
@limiter.limit("10 per hour")
def req():
    print(f"Request request received  {get_remote_address()}")
    request_data = request.get_json()
    # make request
    response = req_factory.makeRequest(
        request_data["url"], request_data["data"], request_data["method"]
    )
    flat_data = optimus.flatten_json(response)

    return jsonify(
        {
            "request": request_data,
            "fields": list(flat_data["out"]),
            "arrays": flat_data["arrays"],
            "response": response,
        }
    )


# Transform endpoint
@app.route("/transform", methods=["POST"])
def transform():
    print(f"Transform request received {get_remote_address()}")
    request_data = request.get_json()

    return jsonify(optimus.mongoTransformation(request_data))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
