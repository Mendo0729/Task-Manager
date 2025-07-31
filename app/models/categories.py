from app.utils.db import db

class Categories(db.Model):
    __tablename__ = "categories"
    __table_args__ = (db.UniqueConstraint('category_name', 'user_id'),)
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
