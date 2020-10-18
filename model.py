from sklearn.ensemble import GradientBoostingRegressor as GBR
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from db_models import Validated


class Model(object):
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.model = self._load_last_checkpoint()
        if self.model is None:
            self.model = GBR(learning_rate=0.2, n_estimators=200, max_depth=2)
            self.train()

    def train(self):
        x, y = self._load_data()
        self.model.fit(x, y)
        self._save_checkpoint()

    def predict(self, x):
        y = self.model.predict([x])
        result = np.clip(y[0], 0, 100)
        return result

    def _load_data(self):
        x = []
        y = []
        validated_data = Validated.query.filter_by(verified=True).all()
        for v in validated_data:
            x.append(v.get_x())
            y.append(v.get_y())
        return x, y

    def _load_last_checkpoint(self):
        model_checkpoint_path = 'data/checkpoint.pkl'
        if os.path.exists(model_checkpoint_path):
            try:
                with open(model_checkpoint_path, 'rb') as checkpoint_file:
                    model = pickle.load(checkpoint_file)
                    self.logger.info('Model loaded successfuly')
            except:
                self.logger.error('Loading model failed, Try to train a new one')
            return model
        return

    def _save_checkpoint(self):
        model_checkpoint_path = 'data/checkpoint.pkl'
        with open(model_checkpoint_path, 'wb') as checkpoint_file:
            pickle.dump(self.model, checkpoint_file)
