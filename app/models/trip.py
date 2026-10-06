from app.utils.extension_util import db
from app.data.constants import TripStatus


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    max_travelers = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=TripStatus.PLANNED)

    participations = db.relationship(
        "TripTraveler",
        back_populates="trip",
        cascade="all, delete-orphan"
    )
    expenses = db.relationship(
        "Expense",
        back_populates="trip",
        cascade="all, delete-orphan"
    )

    def to_json(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "budget": self.budget,
            "max_travelers": self.max_travelers,
            "status": self.status
        }

    def __repr__(self):
        return f"<Trip {self.id} {self.destination}>"