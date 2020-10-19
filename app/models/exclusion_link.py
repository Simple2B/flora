from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class ExclusionLink(db.Model, ModelMixin):

    __tablename__ = "exclusion_links"

    id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey("bids.id"), nullable=False)
    exclusion_id = db.Column(db.Integer, db.ForeignKey("exclusions.id"), nullable=False)
    bid = relationship("Bid")
    exclusion = relationship("Exclusion")

    def __str__(self):
        return "<ExclusionLink: %d>" % self.id
        # return f"{self.exclusion}"
