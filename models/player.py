from db import db


class PlayerModel(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    goals = db.Column(db.Float(precision=2))

    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    club = db.relationship('ClubModelModel')

    def __init__(self, name, goals, club_id):
        self.name = name
        self.goals = goals
        self.club_id = club_id

    def json(self):
        return {'name': self.name, 'goals': self.goals}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
