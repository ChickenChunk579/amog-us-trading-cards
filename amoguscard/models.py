from amoguscard import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    cards = db.relationship('Card', backref='owner', lazy=True)
    credits = db.Column(db.Integer, default=500)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardId = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class TradeOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardId1 = db.Column(db.Integer)
    cardId2 = db.Column(db.Integer)
    isAccepted = db.Column(db.Boolean, default=False)
    senderId = db.Column(db.Integer)
    recieverId = db.Column(db.Integer)

    name = db.Column(db.String(1000))