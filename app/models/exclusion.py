# Exclusion
from app import db
from app.models.utils import ModelMixin


class Exclusion(db.Model, ModelMixin):

    __tablename__ = "exclusions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __str__(self):
        return "<Exclusion: %d>" % self.id
