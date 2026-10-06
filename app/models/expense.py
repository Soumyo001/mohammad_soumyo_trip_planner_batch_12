from app.utils.extension_util import db

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    trip = db.relationship("Trip", back_populates="expenses")

    def to_json(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "title": self.title,
            "amount": self.amount
        }

    def __repr__(self):
        return f"<Expense {self.id} {self.title} {self.amount}>"