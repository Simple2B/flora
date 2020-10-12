from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class Bid(db.Model, ModelMixin):

    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    # procore_id = db.Column(db.Integer)
    title = db.Column(db.String(256), nullable=False)
    client = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(256), nullable=False)

    link_work_items = relationship("LinkWorkItem")
    work_item_groups = relationship("WorkItemGroup")
    attachments = relationship("Attachment")
    clarification_links = relationship("ClarificationLink")
    exclusion_links = relationship("ExclusionLink")

    def __str__(self):
        return "<Bid: %d>" % self.id
