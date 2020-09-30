from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class Attachment(db.Model, ModelMixin):

    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1024), nullable=False)
    file_name = db.Column(db.String(256), nullable=False)
    file_path = db.Column(db.String(256), nullable=False)
    bid_id = db.Column(db.Integer, db.ForeignKey("bids.id"), nullable=False)
    bid = relationship("Bid")

    def __str__(self):
        return "<Attachment: %d>" % self.id
