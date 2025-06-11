import requests
import json

URL = "http://127.0.0.1:8080"


body = {
    "title": "Harry Potter and the Sorcerer's Stone",
    "author": "J. K. Rowling"
}

resp = requests.post(URL + "/wishlist", data=json.dumps(body)).json()
print(json.dumps(resp, indent=2, default=str))

# resp = requests.get(URL + "/wishlist")
# print(json.dumps(resp.json(), indent=2, default=str))

