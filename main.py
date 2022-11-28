
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
# Hello World
def hello_world():
  print('hello world')
  return(jsonify({'message': 'Hello World'}))


# post route to receive data
@app.route('/post', methods=['POST'])
def post():
  print("POST request received")
  data = request.get_json()
  return (jsonify({'data': data}))



if __name__ == '__main__':
  app.run(debug=True)
