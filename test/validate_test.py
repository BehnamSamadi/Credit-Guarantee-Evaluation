import json
from urllib import request
from uuid import uuid4

input_data = {
    'id': 202,
    'desired': 10,
}

params = json.dumps(input_data).encode('utf8')
req = request.Request('http://127.0.0.1:5000/validate', data=params,
                        headers={'content-type': 'application/json'})
response = request.urlopen(req)
print(response.read())
