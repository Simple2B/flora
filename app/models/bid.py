import enum
from datetime import datetime
from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class Bid(db.Model, ModelMixin):

    __tablename__ = "bids"

    class Status(enum.Enum):
        a_new = "New"
        b_draft = "Draft"
        c_submitted = "Submitted"
        d_archived = "Archived"

    id = db.Column(db.Integer, primary_key=True)
    procore_bid_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    client = db.Column(db.String(256), nullable=False)
    address_street = db.Column(db.String(128), nullable=False, default='100 Willoughby Street')
    address_city = db.Column(db.String(128), nullable=False, default='Broklyn, NY, 11201')
    status = db.Column(db.Enum(Status), default=Status.a_new, nullable=False)
    permit_filling_fee = db.Column(db.Float, default=0.0)
    general_conditions = db.Column(db.Float, default=0.0)
    overhead = db.Column(db.Float, default=0.0)
    insurance_tax = db.Column(db.Float, default=0.0)
    profit = db.Column(db.Float, default=0.0)
    bond = db.Column(db.Float, default=0.0)
    subtotal = db.Column(db.Float, default=0.0)
    grand_subtotal = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.String(16), default=(lambda: datetime.today().strftime("%m/%d/%Y"))(), nullable=False)
    time_updated = db.Column(db.Float, default=0.0, nullable=False)

    link_work_items = relationship("LinkWorkItem")
    work_item_groups = relationship("WorkItemGroup")
    attachments = relationship("Attachment")
    clarification_links = relationship("ClarificationLink")
    exclusion_links = relationship("ExclusionLink")

    def __str__(self):
        return f"<Bid:{self.id} - {self.title} - {self.status}>"

    def __repr__(self):
        return f"<Bid:{self.id} - {self.title} - {self.status}>"
