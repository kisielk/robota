from .app import db


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    script = db.Column(db.Text, nullable=False)

    def __init__(self, name, script):
        self.name = name
        self.script = script

    def __repr__(self):
        return '<Job %r>' % self.id


def init_db():
    db.create_all()
