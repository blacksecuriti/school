from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120), index=True)
    Sername = db.Column(db.String(120), index=True)
    scClass = db.Column(db.String(20), index=True)
    tests = db.relationship('Test', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Student {} {} {}>'.format(self.id, self.Name, self.Sername)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unq_id = db.Column(db.String(10))
    anses = db.Column(db.String(50))
    teacher = db.Column(db.String(120), index=True)
    subject = db.Column(db.String(100), index=True)
    result = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime(), index=True)
    stud_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<Test id:{} stud:{} res:{}>'.format(self.id, self.stud_id, self.unq_id)