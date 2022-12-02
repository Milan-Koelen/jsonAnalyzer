from flask import Flask, jsonify, request

from lib import optimus, req_factory

app = Flask(__name__)

@app.route("/")
# Hello World
def hello_world():
    print("hello world")
    
    return jsonify({"message": "Hello World"})

# endpoint to flatten json
@app.route("/flatten", methods=["POST"])
def flatten():
    print("Flatten request received")
    data = request.get_json()
    # flatten json
    flat_data = optimus.flatten_json(data)["out"]
    fields = list(set(flat_data.keys()))
    print("==")
    for field in fields:
        print(field)
    print("===---===---===---===---===---===---===\n")
    
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
    arrays = optimus.flatten_json(data)["arrays"]
    print("==")
    print("fields")
    for field in fields:
        print(field)
    print("===---===---===---===---===---===---===\n")
    
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
def req():
    print("Request request received")
    # convert json data to dict
    request_data = request.get_json()
    # make request
    response = req_factory.makeRequest(
        request_data["url"], request_data["data"], request_data["method"]
    )
    # get all fields witout duplicates
    flat_data = optimus.flatten_json(response)["out"]
    arrays = optimus.flatten_json(response)["arrays"]
    # get all fields witout duplicates
    fields = list(set(flat_data.keys()))
    print("=fields=")
    for field in fields:
        print(field)
    print("===---===---===---===---===---===---===\n")
    
    return jsonify(
        {
            "request": request_data,
            "fields": fields,
            "arrays": arrays,
            "response": response,
        }
    )

# Transform endpoint
@app.route("/transform", methods=["POST"])
def transform():
    print("Transform request received")
    request_data = request.get_json()
    transformation = optimus.mongoTransformation(request_data)
    
    return jsonify(transformation)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
