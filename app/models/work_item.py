from app import db
from app.models.utils import ModelMixin


class WorkItem(db.Model, ModelMixin):

    __tablename__ = "work_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    code = db.Column(db.String(64), unique=True, nullable=False)

    def __str__(self):
        return f"<WorkItem: {self.code}[{self.name}] >"
