from app.utils.db import db

class Priorities(db.Model):
    __tablename__ = "priorities"
    priority_id = db.Column(db.Integer, primary_key=True)
    priority_name = db.Column(db.String(50), unique=True, nullable=False)
    priority_level = db.Column(db.Integer, unique=True, nullable=False)
