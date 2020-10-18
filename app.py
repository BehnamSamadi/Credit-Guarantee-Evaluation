from flask import Flask, request, jsonify
from db_models import db, Validated
from log import setup_logger
from datetime import datetime
from utils import parse_inference_input, \
                 parse_validation_input, \
                 create_response
from model import Model


app = Flask('Credit Eval app')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/db.sqlite"
db.init_app(app)
db.app = app
logger = app.logger
setup_logger(logger)
model = Model(db, logger)

@app.route('/inference', methods=['POST'])
def inference():
    req = parse_inference_input(request.json)
    if req['error']:
        data = {    
                    'request_id': req['id'],
                    'response_id': None,
                    'success': False,
                    'result': None,
                    'message': 'error: '+str(req['error'])
                }
        return create_response(data)
    x = req['data']
    y = model.predict(x)

    record = Validated(date=datetime.now(), request_id=req['id'],
                        param1=x[0], param2=x[1], param3=x[2], 
                        param4=x[3], param5=x[4], param6=x[5],
                        desired=y, verified=False)
    db.session.add(record)
    db.session.commit()

    response_id = record.id
    # logger.info('Prediction for {} : {}'.format(x, y))
    data = {
                'request_id': req['id'],
                'response_id': response_id,
                'success': True,
                'result': round(y, 2),
                'message': 'done successfuly'
            }
    return create_response(data)    


@app.route('/validate', methods=['POST'])
def validate():
    req = parse_validation_input(request.json)
    if req['error']:
        data = {
                    'request_id': req['id'],
                    'success': False,
                    'result': None,
                    'message': 'error: '+str(req['error'])
                }
        return create_response(data)

    val = Validated.query.filter_by(id=req['id']).first()
    if val is None:
        data = {
            'success': False,
            'message': 'error: ' + 'id not matching'
        }
    else:
        val.desired = req['desired']
        val.verified = True
        try:
            db.session.commit()
            model.train()
            data = {    
                        'success': True,
                        'message': 'Model trained with new data'
                    }
        except Exception as e:
            logger.info('Error Training: '+ str(e))
            data = {    
                        'success': False,
                        'message': 'Model trained Failed'
                    }    
    return create_response(data)


if __name__ == "__main__":
    app.run("0.0.0.0")

