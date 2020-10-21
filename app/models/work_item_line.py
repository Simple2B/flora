from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class WorkItemLine(db.Model, ModelMixin):

    __tablename__ = "work_item_lines"

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(256), default='', nullable=False)
    description = db.Column(db.String(1024), default='', nullable=True)
    price = db.Column(db.Float, default=0, nullable=False)
    unit = db.Column(db.String(16), default='LS', nullable=False)
    quantity = db.Column(db.Float, default=1, nullable=False)
    tdb = db.Column(db.Boolean, default=False)
    link_work_items_id = db.Column(
        db.Integer, db.ForeignKey("link_work_items.id"), nullable=False
    )
    link_work_item = relationship("LinkWorkItem")

    def __str__(self):
        return "<WorkItemLine: %d>" % self.id
