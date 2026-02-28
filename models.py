from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# -------------------------
# USER MODEL
# -------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    habits = db.relationship("Habit", back_populates="user", cascade="all, delete")


# -------------------------
# HABIT MODEL
# -------------------------
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="habits")

    logs = db.relationship("HabitLog", back_populates="habit", cascade="all, delete")

    def current_streak(self):
        streak = 0
        for log in sorted(self.logs, key=lambda x: x.date, reverse=True):
            if log.completed:
                streak += 1
            else:
                break
        return streak

