from db_models import Validated
from app import db
import pandas as pd
from datetime import datetime


if __name__ == "__main__":
    
    db.create_all()

    df = pd.read_csv('data/data.csv')
    data = df.to_numpy()[:, 1:]
    data_x, data_y = data[:, :-1], data[:, -1]
    for x, y in zip(data_x, data_y):
        val_data = Validated(date=datetime.now(), request_id='initial',
                            param1=x[0], param2=x[1], param3=x[2],
                            param4=x[3], param5=x[4], param6=x[5],
                            desired=y, verified=True)
        db.session.add(val_data)
    db.session.commit()