from flask_restful import Api, Resource, reqparse
from .models import *
from datetime import datetime

api= Api()

# parser for campaign
campaign_parser = reqparse.RequestParser()
campaign_parser.add_argument("name")
campaign_parser.add_argument("description")
campaign_parser.add_argument("goals")
campaign_parser.add_argument("niche")
campaign_parser.add_argument("visibility")
campaign_parser.add_argument("budget")
campaign_parser.add_argument("start_date")
campaign_parser.add_argument("end_date")


class campaignApi(Resource):

    def get(self,spon_id):
        campaigns= Campaigns.query.filter_by(spon_id=spon_id).all()
        sponsor_campaign=[]
        for campaign in campaigns:
            campaign_details={}
            campaign_details['campaign_id'] = campaign.campaign_id
            campaign_details['name']=campaign.name
            campaign_details['description']=campaign.description
            campaign_details['goals']=campaign.goals
            campaign_details['niche']=campaign.niche
            campaign_details['visibility']=campaign.visibility
            campaign_details['budget']=campaign.budget
            campaign_details['start_date']= campaign.start_date.strftime('%Y-%m-%d')
            campaign_details['end_date']=campaign.end_date.strftime('%Y-%m-%d')
            sponsor_campaign.append(campaign_details)

        return sponsor_campaign
    
    def post(self,spon_id):
        campaign_data= campaign_parser.parse_args()
        start_date = datetime.strptime(campaign_data["start_date"], '%Y-%m-%d').date()
        end_date = datetime.strptime(campaign_data["end_date"], '%Y-%m-%d').date()
        camp_name= campaign_data["name"]

        name= camp_name.replace(" ", "")
        visibility= campaign_data["visibility"]
        if visibility=="public":
            niche= None
        else:
            niche= campaign_data["niche"]

        sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
        spon_name= sponsor.name.replace(" ", "")
        camp_search= name + " " + spon_name + " "
        if niche!=None:
            camp_search+= niche 
        new_camp= Campaigns(name=name, description=campaign_data["description"], goals=campaign_data["goals"], visibility=campaign_data["visibility"],niche=niche, start_date=start_date, end_date=end_date, budget=campaign_data["budget"], spon_id=spon_id, camp_search=camp_search)
        db.session.add(new_camp)
        db.session.commit()
        return "Campaign Created", 201
    
    def put(self, camp_id):
        campaign_data= campaign_parser.parse_args()
        campaign= Campaigns.query.filter_by(campaign_id=camp_id).first()
        if campaign:
            campaign.name= campaign_data["name"]
            name= campaign.name.replace(" ", "")
            campaign.description= campaign_data["description"]
            campaign.goals= campaign_data["goals"]
            campaign.budget= campaign_data["budget"]
            campaign.visibility= campaign_data["visibility"]
            start_date_str = campaign_data["start_date"]
            end_date_str = campaign_data["end_date"]
            try:
                campaign.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                campaign.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

            if campaign.visibility=="public":
                campaign.niche= None
            else:
                campaign.niche= campaign_data["niche"]

            sponsor= Sponsors.query.filter_by(spon_id=campaign.spon_id).first()
            spon_name= sponsor.name.replace(" ", "")
            campaign.camp_search= name + " " + spon_name + " "
            if campaign.visibility=="private":
                campaign.camp_search+= campaign.niche 
            db.session.commit()
            return "Campaign updated", 200
        else:
            return "Campaign not found", 400
        
    def delete(self, camp_id):
        campaign= Campaigns.query.filter_by(campaign_id=camp_id).first()
        if campaign:
            db.session.delete(campaign)
            db.session.commit()
            return "Campaign deleted", 200
        else:
            return "Campaign not found", 400

api.add_resource(campaignApi,"/api/campaign/<int:spon_id>", "/api/campaign/update/<int:camp_id>", "/api/campaign/delete/<int:camp_id>")

# parser for influencer
influencer_parser = reqparse.RequestParser()
influencer_parser.add_argument("username")
influencer_parser.add_argument("pwd")
influencer_parser.add_argument("cpwd")
influencer_parser.add_argument("f_name")
influencer_parser.add_argument("l_name")
influencer_parser.add_argument("niche")
influencer_parser.add_argument("platforms")

class influencerApi(Resource):
    
    def get(self, influ_id):
        influencer= Influencers.query.filter_by(influ_id=influ_id).first()
        if influencer:
                influencer_details={}
                influencer_details['influ_id'] = influencer.influ_id
                influencer_details['f_name']=influencer.f_name
                influencer_details['l_name']=influencer.l_name
                influencer_details['niche']=influencer.niche
                influencer_details['platforms']=influencer.platforms
                influencer_details['flagged']=influencer.flagged
                return influencer_details
        else:
            return "Influencer not found", 400
    
    def post(self):
        influencer_data= influencer_parser.parse_args()
        username= influencer_data["username"]
        influencer= Influencers.query.filter_by(username= username).first()
        if influencer:
            return {"message": "Username already exists"}, 400
        else:
            if influencer_data["cpwd"]==influencer_data["pwd"]:
                platforms= influencer_data["platforms"]
                platform= platforms.split(",")

                influ_search= influencer_data["f_name"]+influencer_data["l_name"]+" " + influencer_data["niche"] + " "+" ".join(platform) 
                new_influencer= Influencers(username=influencer_data["username"],f_name=influencer_data["f_name"], l_name=influencer_data["l_name"], niche=influencer_data["niche"], platforms=influencer_data["platforms"], pwd=influencer_data["pwd"], influ_search=influ_search)
                db.session.add(new_influencer)
                db.session.commit()
                return "Influencer Created", 201
            else:
                return {"message": "passwords do not match"}, 401

    
    def put(self, influ_id):
        influencer_data= influencer_parser.parse_args()
        influencer= Influencers.query.filter_by(influ_id=influ_id).first()
        if influencer:
            influencer.f_name= influencer_data["f_name"]
            influencer.l_name= influencer_data["l_name"]
            influencer.niche= influencer_data["niche"]
            influencer.platforms= influencer_data["platforms"]
            platforms= influencer_data["platforms"]
            platform= platforms.split(",")
            influencer.influ_search= influencer_data["f_name"]+influencer_data["l_name"]+" "+influencer_data["niche"] + " "+" ".join(platform) 
            db.session.commit()
            return "Influencer updated", 200
        else:
            return "Influencer not found", 400
    def delete(self,influ_id):
        influencer= Influencers.query.filter_by(influ_id=influ_id).first()
        if influencer:
            db.session.delete(influencer)
            db.session.commit()
            return "Influencer deleted", 200
        else:
            return "Influencer not found", 400

api.add_resource(influencerApi,"/api/influencer","/api/influencer/<int:influ_id>", "/api/influencer/update/<int:influ_id>", "/api/influencer/delete/<int:influ_id>")

# parser for sponsor
sponsor_parser = reqparse.RequestParser()
sponsor_parser.add_argument("username")
sponsor_parser.add_argument("pwd")
sponsor_parser.add_argument("cpwd")
sponsor_parser.add_argument("name")
sponsor_parser.add_argument("industry")

class sponsorApi(Resource):
    
    def get(self, spon_id):
        sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
        if sponsor:
            sponsor_details={}
            sponsor_details['spon_id'] = sponsor.spon_id
            sponsor_details['name']=sponsor.name
            sponsor_details['industry']=sponsor.industry
            sponsor_details['flagged']=sponsor.flagged

            return sponsor_details
        else:
            return "Sponsor not found", 400
    
    def post(self):
        sponsor_data= sponsor_parser.parse_args()
        sponsor= Sponsors.query.filter_by(username= sponsor_data["username"]).first()
        if sponsor:
            return {"message": "Username already exists"}, 400
        else:
            if sponsor_data["cpwd"]==sponsor_data["pwd"]:

                spon_search= sponsor_data["name"]+" " + sponsor_data["industry"]
                new_sponsor= Sponsors(username=sponsor_data["username"],name=sponsor_data["name"], pwd=sponsor_data["pwd"], industry=sponsor_data["industry"], spon_search=spon_search)
                db.session.add(new_sponsor)
                db.session.commit()
                return "Sponsor Created", 201
            else:
                return {"message": "passwords do not match"}, 401

    
    def put(self, spon_id):
        sponsor_data= sponsor_parser.parse_args()
        sponsor= Sponsors.query.filter_by(spon_id= spon_id).first()
        if sponsor:
            sponsor.name= sponsor_data["name"]
            sponsor.industry= sponsor_data["industry"]
            sponsor.spon_search= sponsor_data["name"]+" " + sponsor_data["industry"]
            db.session.commit()
            return "Sponsor updated", 200
        else:
            return "Sponsor not found", 400

    def delete(self,spon_id):
        sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
        if sponsor:
            db.session.delete(sponsor)
            db.session.commit()
            return "Sponsor deleted", 200
        else:
            return "Sponsor not found", 400

api.add_resource(sponsorApi,"/api/sponsor","/api/sponsor/<int:spon_id>", "/api/sponsor/update/<int:spon_id>", "/api/sponsor/delete/<int:spon_id>")