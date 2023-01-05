from . import db
from flask_login import UserMixin
booking = db.Table('booking',
    db.Column('tourist_id', db.Integer, db.ForeignKey('tourist.id')),
    db.Column('plan_id', db.Integer, db.ForeignKey('trip_plan.id'))
    
)
class Tourist(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    blogs = db.relationship('BlogPost', backref='tourist', lazy=True)
    reservation = db.relationship('TripPlan', secondary='booking', backref='booked', lazy=True)
    def __repr__(self) -> str:
        return "<Tourist %r>" % self.email

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tourist_id = db.Column(db.Integer, db.ForeignKey('tourist.id'), nullable=False)
    date_posted = db.Column(db.DateTime)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    pic = db.Column(db.Text, nullable=False)
    pic_name = db.Column(db.Text)
    mimetype = db.Column(db.Text)

    def __repr__(self) -> str:
        return super().__repr__()

class TripPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transport = db.Column(db.String(10), nullable=False)
    roomtype = db.Column(db.String(20),nullable=False)
    priceid = db.Column(db.String(50), nullable=False)