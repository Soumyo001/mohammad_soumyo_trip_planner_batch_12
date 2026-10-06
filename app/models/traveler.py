from app.utils.extension_util import db

class Traveler(db.Model):
    __tablename__ = "travelers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)

    participations = db.relationship(
        "TripTraveler",
        back_populates="traveler",
        cascade="all, delete-orphan"
    )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    def __repr__(self):
        return f"<Traveler {self.id} {self.email}>"