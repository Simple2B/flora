from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class ClarificationLink(db.Model, ModelMixin):

    __tablename__ = 'clarification_links'

    id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey("bids.id"), nullable=False)
    bid = relationship("Bid")
    clarification_id = db.Column(db.Integer, db.ForeignKey("clarifications.id"), nullable=False)
    clarification = relationship("Clarification")

    def __str__(self):
        return '<ClarificationLink: %d>' % self.id
