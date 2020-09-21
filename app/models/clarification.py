from app import db
from app.models.utils import ModelMixin


class Clarification(db.Model, ModelMixin):

    __tablename__ = 'clarifications'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=True)

    def __str__(self):
        return '<Clarification: %d>' % self.id
