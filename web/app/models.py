from app import db
from datetime import datetime, timedelta
import uuid

class Summary(db.Model):

    __tablename__ = 'run_summaries'
    run_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    total_distance = db.Column(db.Integer)
    step_count = db.Column(db.Integer)

    def populate(self, form):
        self.user_id = form['user_id']
        self.run_id = form['run_id']
        self.start_time = datetime.now() - timedelta(seconds=int(form['duration']))#datetime.strptime(form['start_time'], '%m/%d/%y %H:%M:%S') #POPULATE USING DURATION   
        self.end_time = datetime.now() #datetime.strptime(form['end_time'], '%m/%d/%y %H:%M:%S')
        self.total_distance = form['total_distance']
        self.step_count = form['step_count']

    def serialize(self):
        return {
            "user_id": self.user_id,
            "run_id": self.run_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_distance": self.total_distance,
            "step_count": self.step_count
        }


class Heart_Rate(db.Model):

    __tablename__ = 'heart_rates'
    _id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String)
    time_stamp = db.Column(db.DateTime)
    heart_rate = db.Column(db.Integer)

    def populate(self, form):
        self._id = str(uuid.uuid4())
        self.user_id = form['user_id']
        self.time_stamp = datetime.strptime(form['time_stamp'], '%m/%d/%y %H:%M:%S')
        self.heart_rate = form['heart_rate']

    def serialize(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "time_stamp": self.time_stamp,
            "heart_rate": self.heart_rate
        }

class Map(db.Model):
    __tablename__ = 'maps'
    _id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String)
    run_id = db.Column(db.String)
    time_stamp = db.Column(db.DateTime)
    lat = db.Column(db.String)
    lon = db.Column(db.String)

    def populate(self, form):
        self._id = str(uuid.uuid4())
        self.user_id = form['user_id']
        self.run_id = form['run_id']
        self.time_stamp = datetime.now()
        self.lat = form['lat']
        self.lon = form['lon']

    def serialize(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "run_id": self.run_id,
            "time_stamp": self.time_stamp,
            "lat": self.lat,
            "lon": self.lon
        }