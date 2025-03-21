from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PayerGroup(db.Model):
    __tablename__ = 'payer_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    display_name = db.Column(db.String(100))
    payers = db.relationship('Payer', backref='group', lazy=True)

class Payer(db.Model):
    __tablename__ = 'payers'
    id = db.Column(db.Integer, primary_key=True)
    canonical_name = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('payer_groups.id'), nullable=False)
    payer_details = db.relationship('PayerDetail', backref='payer', lazy=True)

class PayerDetail(db.Model):
    __tablename__ = 'payer_details'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    raw_name = db.Column(db.String(100), nullable=False)
    payer_number = db.Column(db.String(50))  # Ensure this line is present
    ein = db.Column(db.String(20))
    payer_id = db.Column(db.Integer, db.ForeignKey('payers.id'))  # Foreign key to Payer