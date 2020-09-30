from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class WorkItemGroup(db.Model, ModelMixin):

    __tablename__ = "work_item_groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    bid_id = db.Column(db.Integer, db.ForeignKey("bids.id"))
    link_work_item_id = db.Column(db.Integer, db.ForeignKey("link_work_items.id"))
    bid = relationship("Bid")
    link_work_item = relationship("LinkWorkItem")

    def __str__(self):
        return "<WorkItemGroup: %s>" % self.name
