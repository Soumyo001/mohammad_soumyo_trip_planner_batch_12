from app.utils.extension_util import db

class TripTraveler(db.Model):
    __tablename__ = "trip_travelers"
    __table_args__ = (
        db.UniqueConstraint("trip_id", "traveler_id", name="uq_trip_traveler"),
    )

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)
    traveler_id = db.Column(db.Integer, db.ForeignKey("travelers.id"), nullable=False)

    trip = db.relationship("Trip", back_populates="participations")
    traveler = db.relationship("Traveler", back_populates="participations")

    def __repr__(self):
        return f"<TripTraveler trip_id={self.trip_id} traveler_id={self.traveler_id}>"