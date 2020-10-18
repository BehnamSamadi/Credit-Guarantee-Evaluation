import json
from urllib import request
from uuid import uuid4

input_data = {
    'id': str(uuid4()),
    'data': {
        'param1': 10,
        'param2': 10,
        'param3': 10,
        'param4': 10,
        'param5': 10,
        'param6': 10,
    }
}

params = json.dumps(input_data).encode('utf8')
req = request.Request('http://127.0.0.1:5000/inference', data=params,
                        headers={'content-type': 'application/json'})
response = request.urlopen(req)
print(response.read())
