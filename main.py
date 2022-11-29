from flask import Flask, jsonify, request

from lib import optimus

app = Flask(__name__)


@app.route("/")
# Hello World
def hello_world():
    print("hello world")
    return jsonify({"message": "Hello World"})


# post route to receive data
@app.route("/post", methods=["POST"])
def post():
    print("POST request received")
    data = request.get_json()
    return jsonify({"data": data})


# endpoint to flatten json
@app.route("/flatten", methods=["POST"])
def flatten():
    print("Flatten request received")
    data = request.get_json()
    # flatten json
    flat_data = optimus.flatten_json(data)["out"]
    return jsonify(flat_data)


# endpoint to find all fields in json
@app.route("/fields", methods=["POST"])
def fields():
    print("Fields request received")
    data = request.get_json()
    # flatten json
    flat_data = optimus.flatten_json(data)["out"]
    # get all fields witout duplicates
    fields = list(set(flat_data.keys()))
    return jsonify({"fields": fields})


# endpoint to find depth of json
@app.route("/depth", methods=["POST"])
def depth():
    print("Depth request received")
    data = request.get_json()
    # flatten json
    depth = optimus.flatten_json(data)["depth"]
    # get all fields witout duplicates
    # get depth of json
    return jsonify({"depth": depth})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
