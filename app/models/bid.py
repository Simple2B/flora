from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class Bid(db.Model, ModelMixin):

    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    link_work_items = relationship("WorkItemLine")
    work_item_groups = relationship("WorkItemGroup")
    attachments = relationship("Attachment")
    clarification_links = relationship("ClarificationLink")
    exclusion_links = relationship("ExclusionLink")

    def __str__(self):
        return "<Bid: %d>" % self.id
