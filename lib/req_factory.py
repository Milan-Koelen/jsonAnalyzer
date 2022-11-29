import requests as request

# CREATE REQUEST OBJECT AND MAKE REQUEST


def makeRequest(url: str, data: dict, method: str):
    print(f"Making {method} request to {url}")
    if method == "POST":
        response = request.post(url, json=data)
    elif method == "GET":
        response = request.get(url)
    else:
        print("Invalid method")
        return
    return response.json()
