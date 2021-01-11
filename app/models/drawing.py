from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class Drawing(db.Model, ModelMixin):

    __tablename__ = "drawings"

    id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey("bids.id"), nullable=False)
    bid = relationship("Bid")
    number = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    revision_number = db.Column(db.String(32), nullable=False)
    updated_at = db.Column(db.Date, nullable=False)
    pdf_url = db.Column(db.String(512), nullable=False)
    png_url = db.Column(db.String(512), nullable=False)

    def __str__(self):
        return "<Drawing: %d>" % self.id
