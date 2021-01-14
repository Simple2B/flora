from app import db
from app.models.utils import ModelMixin


class Alternate(db.Model, ModelMixin):

    __tablename__ = "alternates"

    id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey("bids.id"), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, default=0, nullable=False)
    unit = db.Column(db.String(16), default='LS', nullable=False)
    quantity = db.Column(db.Float, default=1, nullable=False)
    tbd = db.Column(db.Boolean, default=False)

    def __str__(self):
        return f"<Alternate: {self.id} - {self.name}>"
