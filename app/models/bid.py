import enum
from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class Bid(db.Model, ModelMixin):

    __tablename__ = "bids"

    class Status(enum.Enum):
        a_new = "New"
        b_draft = "Draft"
        c_submited = "Submitted"
        d_archived = "Archived"

    id = db.Column(db.Integer, primary_key=True)
    procore_bid_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    client = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Enum(Status), default=Status.a_new, nullable=False)

    link_work_items = relationship("LinkWorkItem")
    work_item_groups = relationship("WorkItemGroup")
    attachments = relationship("Attachment")
    clarification_links = relationship("ClarificationLink")
    exclusion_links = relationship("ExclusionLink")

    def __str__(self):
        return f"<Bid:{self.id} - {self.title} - {self.status}>"

    def __repr__(self):
        return f"<Bid:{self.id} - {self.title} - {self.status}>"
