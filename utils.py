from flask import jsonify


def parse_inference_input(input):
    param_names = ['param1', 'param2', 'param3', 'param4', 'param5', 'param6']
    req = {
        'id': None,
        'data': [],
        'error': [],
    }
    if 'id' in input.keys():
        req['id'] = input['id']
    if 'data' not in input.keys():
        req['error'].append('Request has no data')
        return req
    try:
        data = input['data']
        keys = data.keys()
        for name in param_names:
            if name not in keys:
                req['error'].append('parameters not compelete')
                break
            xi = float(data[name])
            if xi >= 0 and xi <= 100:
                req['data'].append(xi)
            else:
                req['error'].append('parameters are out of standard range')
                break
    except Exception as e:
        print(str(e))
        req['error'].append('parsing parameters failed')
    return req


def parse_validation_input(input):
    req = {
        'id': None,
        'desired': None,
        'error': [],
    }


    if 'id' in input.keys():
        try:
            req['id'] = int(input['id'])
        except:
            req['error'].append('Parsing id value failed')
    else:
        req['error'].append('No id specified')
    
    try:
        if 'desired' not in input.keys():
            req['error'].append('no desired value specified')
        else:
            y = float(input['desired'])
            if y >= 0 and y <= 100:
                req['desired'] = y
            else:
                req['error'].append('desired value is out of standard range')
    except:
        req['error'].append('parsing desired value failed')
    return req

def create_response(data):
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response