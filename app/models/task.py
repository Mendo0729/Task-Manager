from app.utils.db import db
from sqlalchemy.sql import func

class Tasks(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    priority_id = db.Column(db.Integer, db.ForeignKey("priorities.priority_id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.task_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "due_date": str(self.due_date) if self.due_date else None, # Convierte Date a string
            "is_completed": self.is_completed,
            "priority_id": self.priority_id,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat() if self.created_at else None, # Convierte DateTime a ISO format string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None # Convierte DateTime a ISO format string
        }