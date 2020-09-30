from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class LinkWorkItem(db.Model, ModelMixin):

    __tablename__ = "link_work_items"

    id = db.Column(db.Integer, primary_key=True)
    link_work_item_id = db.Column(db.Integer, nullable=False)
    bid_id = db.Column(db.Integer, db.ForeignKey("bids.id"), nullable=False)
    work_item_id = db.Column(db.Integer, db.ForeignKey("work_items.id"), nullable=False)
    bid = relationship("Bid")
    work_item = relationship("WorkItem")
    work_item_group = relationship("WorkItemGroup")

    def __str__(self):
        return "<LinkWorkItem: %d>" % self.id
