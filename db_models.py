from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Validated(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	request_id = db.Column(db.String(64))
	date = db.Column(db.DateTime)
	param1 = db.Column(db.Float)
	param2 = db.Column(db.Float)
	param3 = db.Column(db.Float)
	param4 = db.Column(db.Float)
	param5 = db.Column(db.Float)
	param6 = db.Column(db.Float)
	desired = db.Column(db.Float)
	verified = db.Column(db.Boolean, default=False)
	
	def get_x(self):
			x = [self.param1, self.param2, self.param3, self.param4, self.param5, self.param6]
			return x
	
	def get_y(self):
			return self.desired
