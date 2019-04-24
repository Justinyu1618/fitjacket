from app import db

class Summary(db.Model):

    __tablename__ = "events"

    uid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    host = db.Column(db.String)
    description = db.Column(db.String)
    description_text = db.Column(db.String)
    categories = db.Column(db.String)
    sent_from = db.Column(db.String)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "location": self.location,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "host": self.host,
            "description": self.description,
            "description_text": self.description_text,
            "categories": self.categories,
            "sent_from": self.sent_from
        }