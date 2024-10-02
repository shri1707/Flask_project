from flask_sqlalchemy import SQLAlchemy
from  datetime import date
db= SQLAlchemy()

class Admins(db.Model):
    __tablename__='admins'
    username=db.Column(db.String, primary_key=True)
    pwd=db.Column(db.String, nullable=False)

class Sponsors(db.Model):
    __tablename__='sponsor'
    spon_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String, unique=True, nullable=False)
    pwd=db.Column(db.String, nullable=False)
    name=db.Column(db.String, nullable=False)
    industry=db.Column(db.String, nullable=False)
    flagged= db.Column(db.Boolean, default=False)
    spon_search= db.Column(db.String, nullable=False)
    campaigns= db.relationship("Campaigns", backref="sponsor" ,cascade='all, delete-orphan')

class Influencers(db.Model):
    __tablename__='influencer'
    influ_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String, unique=True, nullable=False)
    pwd=db.Column(db.String, nullable=False)
    f_name=db.Column(db.String, nullable=False)
    l_name=db.Column(db.String)
    niche= db.Column(db.String, nullable=False)
    platforms = db.Column(db.String, nullable=False)
    flagged= db.Column(db.Boolean, default=False)
    influ_search= db.Column(db.String, nullable=False)
    ads= db.relationship('Ads', backref="influencer" ,cascade='all, delete-orphan')
    
class Campaigns(db.Model):
    __tablename__='campaign'
    campaign_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    spon_id=db.Column(db.Integer, db.ForeignKey('sponsor.spon_id'), nullable=False)
    name=db.Column(db.String, nullable=False)
    description=db.Column(db.String, nullable=False)
    goals= db.Column(db.String, nullable=False)
    niche= db.Column(db.String)
    visibility= db.Column(db.String, nullable=False)
    budget= db.Column(db.Integer, nullable=False)
    start_date= db.Column(db.Date, nullable=False, default=date.today)
    end_date= db.Column(db.Date, nullable=False, default=date.today)
    camp_search= db.Column(db.String, nullable=False)
    flagged= db.Column(db.Boolean, default=False)

    ads = db.relationship('Ads', backref='campaign', cascade='all, delete-orphan')

class Ads(db.Model):
    __tablename__='ads'
    ad_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id= db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'),nullable= False )
    influ_id= db.Column(db.Integer, db.ForeignKey('influencer.influ_id'), nullable=False)
    sent_by= db.Column(db.String, nullable=False)
    requirment= db.Column(db.String, nullable=False)
    payment= db.Column(db.Integer, nullable=False)
    status= db.Column(db.String, nullable=False)
    work_confirmation= db.Column(db.Boolean, nullable=False)
    payment_confirmation= db.Column(db.Boolean, nullable=False)
    
