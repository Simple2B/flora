import enum
import time
from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship
from config import BaseConfig as config


class Bid(db.Model, ModelMixin):

    __tablename__ = "bids"

    class ProjectType(enum.Enum):
        a_budget = "Budget"
        b_quote = "Quote"

    class Status(enum.Enum):
        a_new = "New"
        b_draft = "Draft"
        c_submitted = "Submitted"
        d_archived = "Archived"

    id = db.Column(db.Integer, primary_key=True)
    procore_bid_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    client = db.Column(db.String(256), nullable=False)
    vendor_address_street = db.Column(db.String(128), nullable=False, default='163 Spring Street')
    vendor_address_city = db.Column(db.String(128), nullable=False, default='Newton, New Jersey 07860')
    address_street = db.Column(db.String(128), nullable=False, default='100 Willoughby Street')
    address_city = db.Column(db.String(128), nullable=False, default='Broklyn, NY, 11201')
    phone = db.Column(db.String(128), nullable=False, default='(973) 300-0069')
    email = db.Column(db.String(128), nullable=False, default='ealbanese@ddbcontracting.com')
    fax = db.Column(db.String(128), nullable=False, default='973 300-0805')
    contact = db.Column(db.String(128), nullable=False, default='Edward Albanese')
    project_name = db.Column(db.String(128), nullable=False, default='!Unknown project!')
    status = db.Column(db.Enum(Status), default=Status.a_new, nullable=False)

    percent_permit_fee = db.Column(db.Float, default=config.PERCENT_PERMIT_FEE)
    percent_general_condition = db.Column(db.Float, default=config.PERCENT_GENERAL_CONDITION)
    percent_overhead = db.Column(db.Float, default=config.PERCENT_OVERHEAD)
    percent_insurance_tax = db.Column(db.Float, default=config.PERCENT_INSURANCE_TAX)
    percent_profit = db.Column(db.Float, default=config.PERCENT_PROFIT)
    percent_bond = db.Column(db.Float, default=config.PERCENT_BOND)

    permit_filling_fee = db.Column(db.Float, default=0.0)
    general_conditions = db.Column(db.Float, default=0.0)
    overhead = db.Column(db.Float, default=0.0)
    insurance_tax = db.Column(db.Float, default=0.0)
    profit = db.Column(db.Float, default=0.0)
    bond = db.Column(db.Float, default=0.0)
    subtotal = db.Column(db.Float, default=0.0)
    grand_subtotal = db.Column(db.Float, default=0.0)

    permit_filling_fee_tbd = db.Column(db.Boolean, default=False)
    general_conditions_tbd = db.Column(db.Boolean, default=False)
    overhead_tbd = db.Column(db.Boolean, default=False)
    insurance_tax_tbd = db.Column(db.Boolean, default=False)
    profit_tbd = db.Column(db.Boolean, default=False)
    bond_tbd = db.Column(db.Boolean, default=False)

    popularity = db.Column(db.Integer, default=0)
    time_updated = db.Column(db.Float, default=time.time, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    revision = db.Column(db.Integer, default=0)
    project_type = db.Column(db.Enum(ProjectType), default=ProjectType.b_quote, nullable=False)

    link_work_items = relationship("LinkWorkItem")
    work_item_groups = relationship("WorkItemGroup")
    attachments = relationship("Attachment")
    clarification_links = relationship("ClarificationLink")
    exclusion_links = relationship("ExclusionLink")
    drawings = relationship("Drawing")
    alternates = relationship("Alternate")

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Bid:{self.id}({self.procore_bid_id}) [{self.status.value}]>"
