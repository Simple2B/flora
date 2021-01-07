from app import db
from app.models.utils import ModelMixin


class Docx(db.Model, ModelMixin):

    __tablename__ = "docxes"

    id = db.Column(db.Integer, primary_key=True)
    path_to_file = db.Column(db.String, nullable=False)

    def __str__(self):
        return f"<Docx:{self.id} - {self.path_to_file}>"

    def __repr__(self):
        return f"<Docx:{self.id} - {self.path_to_file}>"
