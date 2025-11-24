from database import db
import json

class Cadaver(db.Model):
    __tablename__ = "cadaver"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)

    def to_dict(self):
        try:
            return json.loads(self.data)
        except:
            return None
