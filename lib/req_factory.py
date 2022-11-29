import requests as request

# CREATE REQUEST OBJECT



def makeRequest(url:str, data:dict, method:str):
    print("Making request to {} with data {}".format(url, data))
    if method == "POST":
        response = request.post(url, json=data)
    elif method == "GET":
        response = request.get(url)
    else:
        print("Invalid method")
        return
    print("Response: {}".format(response.json()))
    return "response.json"

  