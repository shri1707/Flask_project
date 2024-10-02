from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
from flask import current_app as app
from backend.models import *
from matplotlib import pyplot as plt
import os
plt.switch_backend('Agg')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        select= request.form.get('type')
        uname= request.form.get('username')
        pwd = request.form.get('pass')
        if select == "admin":
            admin= Admins.query.filter_by(username=uname, pwd=pwd).first()
            if admin:
                camp_summary= fetch_camp()
                return render_template('admin/admin_dash.html', admin= admin, camp=camp_summary, flagged=None)
            else:
                return render_template('index.html', msg="Invalid Credentials, Please try again")
        elif select == "sponsor":
            sponsor= Sponsors.query.filter_by(username=uname, pwd=pwd).first()
            if sponsor: 
                return redirect(url_for('spon_profile', spon_id=sponsor.spon_id))

            else:
                return render_template('index.html', msg="Invalid Credentials, Please try again")
        elif select == "influencer":
            influencer= Influencers.query.filter_by(username=uname, pwd=pwd).first()
            if influencer:
                return redirect(url_for('influencer_profile', influ_id=influencer.influ_id))
            else:
                return render_template('index.html', msg="Invalid Credentials, Please try again")
        else:
            return render_template('index.html', msg="Invalid Credentials, Please try again")
    return render_template('index.html', msg="")


# registrations

@app.route('/influencer_register', methods=['GET', 'POST'])
def influencer_reg():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        uname = request.form.get('uname')
        pwd = request.form.get('pass')
        cpwd = request.form.get('cpass')
        niche = request.form.get('niche')
        flagged= False
        platforms_list = request.form.getlist('platform') 
        platforms = ','.join(platforms_list) 
        influ_search = fname + lname + " " + niche + " " + " ".join(platforms_list)  
        influencer = Influencers.query.filter_by(username=uname).first()
        
        if not influencer:
            if cpwd == pwd:
                new_influencer = Influencers(username=uname, f_name=fname, l_name=lname, niche=niche, pwd=pwd, platforms=platforms, flagged=flagged, influ_search=influ_search)
                db.session.add(new_influencer)
                db.session.commit()

                return render_template('index.html', msg="Influencer registered successfully.")
            else:
                return render_template('influencer_register.html', msg="Passwords do not match.")
        else:
            return render_template('influencer_register.html', msg="Username already exists.")
    
    return render_template('influencer_register.html', msg="")

@app.route('/sponsor_register', methods=['GET', 'POST'])
def sponsor_reg():
        if request.method == 'POST':
            name= request.form.get('name')
            uname= request.form.get('uname')
            pwd = request.form.get('pass')
            cpwd= request.form.get('cpass')
            industry= request.form.get('industry')
            flagged= False
            sponsor= Sponsors.query.filter_by(username=uname).first()


            spon_name= name.replace(" ", "")

            spon_search= name+ " " + industry
            if not sponsor:
                if cpwd==pwd:
                    new_sponsor = Sponsors(username=uname, name=name, industry=industry, pwd=pwd, flagged=flagged, spon_search=spon_search)
                    db.session.add(new_sponsor)
                    db.session.commit()
                    return render_template('index.html', msg="")
                else:
                    return render_template('sponsor_register.html', msg="Passwords do not match")
            else:
                return render_template('sponsor_register.html', msg="Username already exists")
        return render_template('sponsor_register.html', msg="")


# sponsors related
@app.route('/dashboard/campaigns/<int:spon_id>', methods=['GET'])
def get_campaign(spon_id):
    sponsor= fetch_sponsor_camp(spon_id)
    influencers= Influencers.query.all()
    ads= Ads.query.all()
    influ= None
    for ad in ads:
        for influencer in influencers:
            if ad.influ_id==influencer.influ_id:
                influ=influencer

    return render_template('user/sponsor_campaigns.html', campaign=sponsor.campaigns, sponsor=sponsor, influencer=influ) 

@app.route('/dashboard/sponsor/<int:spon_id>', methods= ['GET', 'POST']) 
def spon_profile(spon_id):
    sponsor= fetch_sponsor_camp(spon_id)
    ads= Ads.query.all()
    camps= Campaigns.query.all()
    influencers= Influencers.query.all()
    return render_template('user/sponsor_dash.html', sponsor=sponsor, ads=ads,camps=camps, influencers= influencers)

@app.route('/dashboard/find/<int:spon_id>', methods= ['GET','POST'])
def spon_find(spon_id):
    sponsor= fetch_sponsor_camp(spon_id)
    campaigns= Campaigns.query.filter_by(spon_id=sponsor.spon_id)
    influencers= Influencers.query.all()
    print(influencers)
    influencer= (influencers[0])
    print(influencer.platforms)
    return render_template('user/sponsor_find.html', sponsor=sponsor, campaigns=campaigns, influencers=influencers)

@app.route('/dashboard/sponsor_stat/<int:spon_id>')
def spon_stat(spon_id):
    sponsor= fetch_sponsor_camp(spon_id)
    campaigns= Campaigns.query.filter_by(spon_id=spon_id)
    sponsor_campaign_summary(spon_id)
    ads= Ads.query.all()
    influencers= Influencers.query.all()
    return render_template('user/sponsor_stat.html', sponsor=sponsor, ads=ads, influencers=influencers, campaigns=campaigns)

def sponsor_campaign_summary(spon_id):
    campaigns= Campaigns.query.filter_by(spon_id=spon_id).all()
    print(campaigns)
    labels = ["Completed", "Ongoing", "Pending Requests", "Rejected"]
    path = "static/images/spon_summary/"
    
    for campaign in campaigns:
        completed_ads = Ads.query.filter_by(campaign_id=campaign.campaign_id, status="completed").all()
        accepted_ads = Ads.query.filter_by(campaign_id=campaign.campaign_id, status="accepted").all()
        pending_ads= Ads.query.filter_by(campaign_id=campaign.campaign_id, status="pending").all()
        rejected_ads = Ads.query.filter_by(campaign_id=campaign.campaign_id, status="rejected").all()
        
        print(completed_ads)
        print(accepted_ads)
        cad = len(completed_ads) or 0
        aad = len(accepted_ads) or 0
        pad= len(pending_ads) or 0
        rad= len(rejected_ads) or 0
        data = [cad, aad, pad, rad]
        colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336']

        if campaign.ads:
            plt.bar(labels, data, width=0.3, color=colors)
            plt.savefig(os.path.join(path, f"sponsor_{campaign.campaign_id}.jpg"))
            plt.clf()

    labels=["Flagged Campaigns", "Unflagged Campaigns"]
    flagged_campaigns = Campaigns.query.filter_by(spon_id=spon_id, flagged=True).all()
    unflagged_campaigns = Campaigns.query.filter_by(spon_id=spon_id, flagged=False).all()


    fc= len(flagged_campaigns) or 0
    ufc= len(unflagged_campaigns) or 0
    data =[fc, ufc]
    colors = ['red', 'green']
    plt.bar(labels, data, width=0.3, color= colors)
    plt.savefig(os.path.join(path, f"sponsor_campaign_flagged.jpg"))
    plt.clf()

@app.route('/edit_profile/sponsor/<int:spon_id>', methods= ['GET','POST'])
def edit_sponsor(spon_id):
    if request.method == 'POST':
        new_name=request.form.get('spon_name')
        new_industry= request.form.get('industry')
        spon_name= new_name.replace(" ", "")
        spon_search = spon_name + " " + new_industry
        sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
        sponsor.name=new_name
        sponsor.industry=new_industry
        sponsor.spon_search=spon_search
        db.session.commit()

        campaigns= Campaigns.query.filter_by(spon_id=spon_id).all()
        for campaign in campaigns:
            camp_search = campaign.camp_search
            camp_search_list = camp_search.split(' ')
            camp_search_list[1] = new_name
            camp_search = ' '.join(camp_search_list)

            campaign.camp_search = camp_search
            db.session.commit()
        return redirect(url_for('spon_profile', spon_id=spon_id))

@app.route('/delete/sponsorId/<int:spon_id>', methods=['POST'])
def delete_sponsor(spon_id):
    sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
    db.session.delete(sponsor)
    db.session.commit()
    return redirect(url_for('home'))

def fetch_camp():
    camps= Campaigns.query.all()
    print(camps)
    camp_list={}
    for camp in camps:
        sponsor = Sponsors.query.filter_by(spon_id=camp.spon_id).first()
        sponsor_username= sponsor.username
        if camp.campaign_id not in camp_list.keys():
            camp_list[camp.campaign_id]=[camp.name,camp.goals,camp.visibility, camp.niche, camp.budget, camp.start_date, camp.end_date,camp.flagged,camp.description, sponsor.name, sponsor.flagged]
    print(camp_list)
    return camp_list


def fetch_search_camp(camps):
    camp_list={}
    for camp in camps:
        sponsor = Sponsors.query.filter_by(spon_id=camp.spon_id).first()
        sponsor_username= sponsor.username
        if camp.campaign_id not in camp_list.keys():
            camp_list[camp.campaign_id]=[camp.name,camp.goals,camp.visibility, camp.niche, camp.budget, camp.start_date, camp.end_date,camp.flagged,camp.description, sponsor.name, sponsor.flagged]
    print(camp_list)
    return camp_list

def fetch_sponsor_camp(id):
    sponsor_camp= Sponsors.query.filter_by(spon_id=id).first()
    return sponsor_camp

@app.route('/campaigns/add/<int:spon_id>', methods=['GET', 'POST'])
def add_campaign(spon_id):
    if request.method =='POST':
        campaign = request.form.get('camp_name')
        description= request.form.get('description')
        goals= request.form.get('goals')
        visibility= request.form.get('visibility')
        niche= request.form.get('niche')
        budget= request.form.get('budget')
        start_date_str= request.form.get('start_date')
        end_date_str= request.form.get('end_date')
        flagged= False

        camp_name= campaign.replace(" ", "")

        sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
        spon_name= sponsor.name.replace(" ", "")
        camp_search= camp_name + " " + spon_name + " "
        if niche:
            camp_search+= niche 
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        # print(campaign, description, start_date, end_date)
        new_camp= Campaigns(name=campaign, description=description, goals=goals, visibility=visibility, niche=niche, start_date=start_date, end_date=end_date, budget=budget, spon_id=spon_id, flagged=flagged, camp_search=camp_search)
        db.session.add(new_camp)
        db.session.commit()
        sponsor= fetch_sponsor_camp(spon_id)
        return redirect(url_for('get_campaign', spon_id=spon_id))
@app.route('/campaigns/edit/<int:spon_id>', methods=['GET', 'POST'])
def edit_campaign(spon_id):
    if request.method == 'POST':
        new_campaign = request.form.get('camp_name')
        new_description= request.form.get('description')
        new_goals= request.form.get('goals')
        new_visibility= request.form.get('visibility')
        new_niche= request.form.get('niche')
        new_budget= request.form.get('budget')
        new_start_date_str= request.form.get('start_date')
        new_end_date_str= request.form.get('end_date')
        new_start_date = datetime.strptime(new_start_date_str, '%Y-%m-%d').date()
        new_end_date = datetime.strptime(new_end_date_str, '%Y-%m-%d').date()

        camp_name= new_campaign.replace(" ", "")

        sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
        spon_name= sponsor.name
        camp_search= camp_name + " " + spon_name + " "
        if new_niche:
            camp_search+= new_niche 

        camp_obj= Campaigns.query.filter_by(spon_id=spon_id, name= new_campaign).first()
        camp_obj.name= new_campaign
        camp_obj.description=new_description
        camp_obj.goals=new_goals
        camp_obj.niche=new_niche
        camp_obj.visibility=new_visibility
        camp_obj.budget=new_budget
        camp_obj.start_date=new_start_date
        camp_obj.end_date=new_end_date
        camp_obj.camp_search=camp_search
        db.session.commit()
        sponsor= fetch_sponsor_camp(spon_id)
        return redirect(url_for('get_campaign', spon_id=spon_id))

@app.route('/campaigns/del/<int:spon_id>', methods=['GET', 'POST'])
def del_campaign(spon_id):
        if request.method == 'POST':
            campaign = request.form.get('camp_name')
            camp_obj= Campaigns.query.filter_by(spon_id=spon_id, name= campaign).first()
            db.session.delete(camp_obj)
            db.session.commit()
            sponsor= fetch_sponsor_camp(spon_id)
        return redirect(url_for('get_campaign', spon_id=spon_id))
        

@app.route('/negotiate/sponsor/<int:spon_id>', methods=['GET','POST'])
def negotiate(spon_id):
    if request.method == 'POST':
        negotiation_request= request.form.get('negotiate')
        ad_id= request.form.get('ad_id')
        print(ad_id)
        ad_obj= Ads.query.filter_by(ad_id=ad_id).first()
        ad_obj.payment=negotiation_request
        ad_obj.sent_by="sponsor"
        db.session.commit()
        return redirect(url_for('spon_profile', spon_id=spon_id))
    

@app.route('/ad/delete/<int:spon_id>/<int:ad_id>')
def del_ad(spon_id,ad_id):
    ad= Ads.query.filter_by(ad_id=ad_id).first()
    if ad:
        db.session.delete(ad)
        db.session.commit()
    return redirect(url_for('spon_profile', spon_id=spon_id))


@app.route('/ad/reject/<int:spon_id>/<int:ad_id>')
def reject_ad(spon_id,ad_id):
    ad=Ads.query.filter_by(ad_id=ad_id).first()
    if ad:
        ad.status="rejected"
        db.session.commit()
    return redirect(url_for('spon_profile', spon_id=spon_id))


# influencer related

def influencer_accepted_ads(influ_id):
    ads= Ads.query.filter_by(influ_id=influ_id, status="accepted", payment_confirmation=False)
    print(ads)
    ads_list={}
    for ad in ads:
        campaign = Campaigns.query.filter_by(campaign_id=ad.campaign_id).first()
        campaign_name= campaign.name
        campaign_end= campaign.end_date
        sponsor = Sponsors.query.filter_by(spon_id=campaign.spon_id).first()
        sponsor_username= sponsor.username
        influencer= Influencers.query.filter_by(influ_id=influ_id).first()
        if ad.ad_id not in ads_list.keys():
            ads_list[ad.ad_id]=[ad.ad_id,ad.campaign_id, ad.influ_id , ad.sent_by , ad.requirment , ad.payment, ad.status, ad.work_confirmation, ad.payment_confirmation, sponsor.name, campaign_name, campaign_end, campaign.flagged,influencer.username]
    return ads_list

def influencer_pending_ads(influ_id):
    ads= Ads.query.filter_by(influ_id=influ_id, status="pending", payment_confirmation=False)
    print(ads)
    ads_list={}
    for ad in ads:
        campaign = Campaigns.query.filter_by(campaign_id=ad.campaign_id).first()
        campaign_name= campaign.name
        campaign_end= campaign.end_date
        sponsor = Sponsors.query.filter_by(spon_id=campaign.spon_id).first()
        sponsor_username= sponsor.username
        influencer= Influencers.query.filter_by(influ_id=influ_id).first()
        if ad.ad_id not in ads_list.keys():
            ads_list[ad.ad_id]=[ad.ad_id,ad.campaign_id, ad.influ_id , ad.sent_by , ad.requirment , ad.payment, ad.status, ad.work_confirmation, ad.payment_confirmation, sponsor.name, campaign_name, campaign_end, campaign.flagged, influencer.username]
    print(ads_list)
    return ads_list

def influencer_completed_ads(influ_id):
    ads= Ads.query.filter_by(influ_id=influ_id, status="completed")
    print(ads)
    ads_list={}
    for ad in ads:
        campaign = Campaigns.query.filter_by(campaign_id=ad.campaign_id).first()
        campaign_name= campaign.name
        campaign_end= campaign.end_date
        sponsor = Sponsors.query.filter_by(spon_id=campaign.spon_id).first()
        sponsor_username= sponsor.username
        influencer= Influencers.query.filter_by(influ_id=influ_id).first()
        if ad.ad_id not in ads_list.keys():
            ads_list[ad.ad_id]=[ad.ad_id,ad.campaign_id, ad.influ_id , ad.sent_by , ad.requirment , ad.payment, ad.status, ad.work_confirmation, ad.payment_confirmation, sponsor.name, campaign_name, campaign_end, influencer.username]
    return ads_list

def influencer_rejected_ads(influ_id):
    ads= Ads.query.filter_by(influ_id=influ_id, status="rejected", sent_by="influencer", payment_confirmation=False)
    print(ads)
    ads_list={}
    for ad in ads:
        campaign = Campaigns.query.filter_by(campaign_id=ad.campaign_id).first()
        campaign_name= campaign.name
        campaign_end= campaign.end_date
        sponsor = Sponsors.query.filter_by(spon_id=campaign.spon_id).first()
        sponsor_username= sponsor.username
        influencer= Influencers.query.filter_by(influ_id=influ_id).first()
        if ad.ad_id not in ads_list.keys():
            ads_list[ad.ad_id]=[ad.ad_id,ad.campaign_id, ad.influ_id , ad.sent_by , ad.requirment , ad.payment, ad.status, ad.work_confirmation, ad.payment_confirmation, sponsor.name, campaign_name, campaign_end, influencer.username]
    return ads_list

def advertisements():
    ads= Ads.query.all()
    print(ads)
    ads_list={}
    for ad in ads:
        influencer= Influencers.query.filter_by(influ_id=ad.influ_id).first()
        if ad.ad_id not in ads_list.keys():
            ads_list[ad.ad_id]=[ad.ad_id,ad.campaign_id, ad.influ_id , ad.sent_by , ad.requirment , ad.payment, ad.status, ad.work_confirmation, ad.payment_confirmation, influencer.username]
    print(ads_list)
    return ads_list

@app.route('/dashboard/influencer/<int:influ_id>', methods=['GET', 'POST'])
def influencer_profile(influ_id):
    influencer= Influencers.query.filter_by(influ_id=influ_id).first()
    accepted_ads= influencer_accepted_ads(influencer.influ_id)
    pending_ads= influencer_pending_ads(influencer.influ_id)
    completed_ads= influencer_completed_ads(influencer.influ_id)
    rejected_ads= influencer_rejected_ads(influencer.influ_id)
    return render_template('user/influencer_dash.html',ads=accepted_ads,pending_ads=pending_ads,completed_ads=completed_ads ,rejected_ads=rejected_ads, influencer= influencer)

@app.route('/dashboard/influencer_find/<int:influ_id>', methods=['GET', 'POST'])
def influencer_find(influ_id):
    influencer= Influencers.query.filter_by(influ_id=influ_id).first()
    camp_summary= fetch_camp()
    print(camp_summary)
    return render_template('user/influencer_find.html', influencer=influencer, camp=camp_summary)

@app.route('/dashboard/influencer_stat/<int:influ_id>', methods=['GET','POST'])
def influencer_stat(influ_id):
    influencer=Influencers.query.filter_by(influ_id=influ_id).first()
    get_influencer_summary(influ_id)
    return render_template('user/influencer_stat.html', influencer=influencer)

def get_influencer_summary(influ_id):
    ads= Ads.query.filter_by(influ_id=influ_id).all()
    labels = ["Completed", "Ongoing", "Pending Requests", "Rejected"]
    path = "static/images/influ_summary/"
    
    completed_ads = Ads.query.filter_by(status="completed").all()
    accepted_ads = Ads.query.filter_by(status="accepted").all()
    pending_ads= Ads.query.filter_by(status="pending").all()
    rejected_ads = Ads.query.filter_by(status="rejected").all()
        
    print(completed_ads)
    print(accepted_ads)
    cad = len(completed_ads) or 0
    aad = len(accepted_ads) or 0
    pad= len(pending_ads) or 0
    rad= len(rejected_ads) or 0
    data = [cad, aad, pad, rad]
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336']
    plt.bar(labels, data, width=0.3, color=colors)
    plt.savefig(os.path.join(path, f"{influ_id}.jpg"))
    plt.clf()

        
@app.route('/edit_profile/influencer/<int:influ_id>', methods=['GET','POST'])
def edit_influencer(influ_id):
    if request.method == 'POST':
        influencer= Influencers.query.filter_by(influ_id=influ_id).first()
        influencer.f_name=request.form.get('f_name')
        influencer.l_name= request.form.get('l_name')
        influencer.niche= request.form.get('niche')
        platforms_list= request.form.getlist('platform')
        influencer.platforms=" "
        influencer.platforms= ",".join(platforms_list)
        
        influencer.influ_search = influencer.f_name + influencer.l_name + " " + influencer.niche + " " + " ".join(platforms_list)  

        db.session.commit()
        return redirect(url_for('influencer_profile', influ_id=influencer.influ_id))

@app.route('/delete/influencerId/<int:influ_id>', methods=['POST'])
def delete_influencer(influ_id):
    influencer= Influencers.query.filter_by(influ_id=influ_id).first()
    db.session.delete(influencer)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/negotiate/influencer/<int:influ_id>', methods=['GET','POST'])
def influencer_negotiate(influ_id):
    if request.method == 'POST':
        negotiation_request= request.form.get('negotiate')
        ad_id= request.form.get('ad_id')
        print(ad_id)
        ad_obj= Ads.query.filter_by(ad_id=ad_id).first()
        ad_obj.payment=negotiation_request
        ad_obj.sent_by="influencer"
        db.session.commit()
        return redirect(url_for('influencer_profile', influ_id=influ_id))
    
@app.route('/influencer/ad/delete/<int:influ_id>/<int:ad_id>')
def influencer_del_ad(influ_id,ad_id):
    ad= Ads.query.filter_by(ad_id=ad_id).first()
    if ad:
        db.session.delete(ad)
        db.session.commit()
    return redirect(url_for('influencer_profile', influ_id=influ_id))

# admin related
@app.route('/dashboard/admin/<username>', methods=['GET', 'POST'])
def admin_profile(username):
    camp_summary= fetch_camp()
    influencers= Influencers.query.all()
    sponsors= Sponsors.query.all()
    # campaign= Campaigns.query.all()
    admin= Admins.query.filter_by(username=username).first()
    return render_template('admin/admin_dash.html', admin=admin, camp=camp_summary, influencers=influencers,sponsors=sponsors)

@app.route('/dashboard/admin_find/<username>', methods=['GET', 'POST'])
def admin_campaigns(username):
    admin= Admins.query.filter_by(username=username).first()
    camp_summary= fetch_camp()
    print(camp_summary)
    influencers= Influencers.query.all()
    sponsors= Sponsors.query.all()
    return render_template("admin/admin_find.html", admin=admin, camp=camp_summary, influencers=influencers, sponsors=sponsors )


@app.route('/dashboard/admin_stat/<username>', methods=['GET', 'POST'])
def admin_stat(username):
    admin = Admins.query.filter_by(username=username).first()
    campaigns = Campaigns.query.all()
    generate_campaign_summary(campaigns)
    generate_user_summary(username)
    return render_template('admin/admin_stat.html', admin=admin, campaigns=campaigns)

def generate_campaign_summary(campaigns):
    labels = ["Completed", "Ongoing", "Pending Requests", "Rejected"]
    path = "static/images/admin_summary/"
    if not os.path.exists(path):
        os.makedirs(path)
    
    for campaign in campaigns:
        completed_ads = Ads.query.filter_by(campaign_id=campaign.campaign_id, status="completed").all()
        accepted_ads = Ads.query.filter_by(campaign_id=campaign.campaign_id, status="accepted").all()
        pending_ads= Ads.query.filter_by(campaign_id=campaign.campaign_id, status="pending").all()
        rejected_ads = Ads.query.filter_by(campaign_id=campaign.campaign_id, status="rejected").all()
        
        print(completed_ads)
        print(accepted_ads)
        cad = len(completed_ads) or 0
        aad = len(accepted_ads) or 0
        pad= len(pending_ads) or 0
        rad= len(rejected_ads) or 0
        data = [cad, aad, pad, rad]
        colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336']

        if campaign.ads:
            plt.bar(labels, data, width=0.3, color=colors)
            plt.savefig(os.path.join(path, f"{campaign.campaign_id}.jpg"))
            plt.clf()

    labels=["Flagged Campaigns", "Unflagged Campaigns"]
    
    flagged_campaigns = Campaigns.query.filter_by(flagged=True).all()
    unflagged_campaigns = Campaigns.query.filter_by(flagged=False).all()

    fc= len(flagged_campaigns) or 0
    ufc= len(unflagged_campaigns) or 0
    data =[fc, ufc]
    colors = ['red', 'green']
    plt.bar(labels, data, width=0.3, color= colors)
    plt.savefig(os.path.join(path, f"campaign_flagged.jpg"))
    plt.clf()
    
def generate_user_summary(username):
    admin= Admins.query.filter_by(username=username).first()

    labels=["Influencers", "Sponsors"]
    path= "static/images/admin_summary/"
    if not os.path.exists(path):
        os.makedirs(path)

    influencers= Influencers.query.all()
    sponsors= Sponsors.query.all()
    
    influ_size= len(influencers) or 0
    spon_size= len(sponsors) or 0
    data=[len(influencers), len(sponsors)]
    colors = ["lightblue", "lightgreen"]
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig(os.path.join(path, f"{admin.username}.jpg"))
    plt.clf()

    labels=["Influencers", "Sponsors"]
    flagged_influ= Influencers.query.filter_by(flagged= True).all()
    unflagged_influ= Influencers.query.filter_by(flagged= False).all()

    flagged_spon= Sponsors.query.filter_by(flagged= True).all()
    unflagged_spon= Sponsors.query.filter_by(flagged= False).all()
    
    
    flagged_influ_size= len(flagged_influ) or 0
    unflagged_influ_size= len(unflagged_influ) or 0
    flagged_spon_size= len(flagged_spon) or 0
    unflagged_spon_size= len(unflagged_spon) or 0

    flagged_sizes = [flagged_influ_size, flagged_spon_size]
    unflagged_sizes = [unflagged_influ_size, unflagged_spon_size]
    
    # Create Stacked Bar Chart
    bar_width = 0.5
    index = range(len(labels))
    
    fig, ax = plt.subplots()
    
    # Plot bars
    bar1 = ax.bar(index, flagged_sizes, bar_width, label='Flagged', color='lightblue')
    bar2 = ax.bar(index, unflagged_sizes, bar_width, bottom=flagged_sizes, label='Unflagged', color='lightgreen')
    
    for i in index:
        ax.text(i, flagged_sizes[i] / 2, str(flagged_sizes[i]), ha='center', va='center', color='black', fontsize=10)
        ax.text(i, flagged_sizes[i] + unflagged_sizes[i] / 2, str(unflagged_sizes[i]), ha='center', va='center', color='black', fontsize=10)
    # Add labels and title
    ax.set_xlabel('Categories')
    ax.set_ylabel('Count')
    ax.set_title('Flagged vs Unflagged')
    ax.set_xticks(index)
    ax.set_xticklabels(labels)
    ax.legend()
    
    # Save and clear plot
    plt.savefig(os.path.join(path, f"{admin.username}_flagged_vs_unflagged.jpg"))
    plt.clf()


# Ad related
@app.route("/ad/add/<int:spon_id>",methods=["GET","POST"])
def ad_req(spon_id):
    if request.method=="POST":
        influ_id=request.form.get("influ_id")
        camp_name=request.form.get("camp_name")
        requirment=request.form.get("requirment")
        payment=request.form.get("payment")
        sent_by="sponsor"
        status="pending"
        work_confirmation=False
        payment_confirmation=False
        campaign= Campaigns.query.filter_by(name=camp_name).first()
        if campaign:
            ad = Ads(
                influ_id=influ_id,
                campaign_id=campaign.campaign_id,
                sent_by=sent_by,
                requirment=requirment,
                payment=payment,
                status=status,
                work_confirmation=work_confirmation,
                payment_confirmation=payment_confirmation
            )
            db.session.add(ad)
            db.session.commit()

        sponsor= fetch_sponsor_camp(spon_id)
        return redirect(url_for('spon_find', spon_id=spon_id))
    
@app.route("/advertisment/add/<int:influ_id>",methods=["GET","POST"])
def ad_influ_req(influ_id):
    if request.method=="POST":
        camp_name=request.form.get("camp_name")
        requirment=request.form.get("requirment")
        payment=request.form.get("payment")
        sent_by="influencer"
        status="pending"
        work_confirmation=False
        payment_confirmation=False
        campaign= Campaigns.query.filter_by(name=camp_name).first()
        if campaign:
            ad = Ads(
                influ_id=influ_id,
                campaign_id=campaign.campaign_id,
                sent_by=sent_by,
                requirment=requirment,
                payment=payment,
                status=status,
                work_confirmation=work_confirmation,
                payment_confirmation=payment_confirmation
            )
        db.session.add(ad)
        db.session.commit()
        return redirect(url_for('influencer_find', influ_id=influ_id))

@app.route('/complete/ad/<int:influ_id>/<int:ad_id>')
def ad_complete(influ_id,ad_id):
    ad=Ads.query.filter_by(ad_id=ad_id).first()
    if ad:
        ad.status="completed"
        db.session.commit()
    return redirect(url_for('influencer_profile', influ_id=influ_id))

@app.route('/ad/accept/<int:influ_id>/<int:ad_id>')
def influencer_ad_accept(influ_id,ad_id):
    ad=Ads.query.filter_by(ad_id=ad_id).first()
    if ad:
        ad.status="accepted"
        db.session.commit()
    return redirect(url_for('influencer_profile', influ_id=influ_id))

@app.route('/sponsor/ad/accept/<int:spon_id>/<int:ad_id>')
def ad_accept(spon_id, ad_id):
    ad = Ads.query.filter_by(ad_id=ad_id).first()
    if ad:
        ad.status = "accepted"
        db.session.commit()
    return redirect(url_for('spon_profile', spon_id=spon_id))

@app.route('/ad/payment/<int:spon_id>/<int:ad_id>')
def ad_payment(spon_id, ad_id):
    ad = Ads.query.filter_by(ad_id=ad_id).first()
    if ad:
        ad.payment_confirmation=True
        db.session.commit()
    return redirect(url_for('spon_profile', spon_id=spon_id))


@app.route('/ad/reject/influencer/<int:influ_id>/<int:ad_id>')
def ad_reject(influ_id,ad_id):
    ad=Ads.query.filter_by(ad_id=ad_id).first()
    if ad:
        ad.status="rejected"
        db.session.commit()
    return redirect(url_for('influencer_profile', influ_id=influ_id))

@app.route('/edit_ad/sponsor/<int:spon_id>', methods=['POST'])
def edit_ad(spon_id):
    if request.method == 'POST':
        ad_id=request.form.get('ad_id')
        new_requirment=request.form.get('requirment')
        new_payment= request.form.get('payment')

        ad_obj=Ads.query.filter_by(ad_id=ad_id).first()
        ad_obj.requirment=new_requirment
        ad_obj.payment=new_payment
        db.session.commit()
        return redirect(url_for('spon_profile', spon_id=spon_id))

@app.route('/edit_ad/influencer/<int:influ_id>', methods=['POST'])
def influencer_edit_ad(influ_id):
    if request.method == 'POST':
        ad_id=request.form.get('ad_id')
        new_requirment=request.form.get('requirment')
        new_payment= request.form.get('payment')

        ad_obj=Ads.query.filter_by(ad_id=ad_id).first()
        ad_obj.requirment=new_requirment
        ad_obj.payment=new_payment
        db.session.commit()
        return redirect(url_for('influencer_profile', influ_id=influ_id))


#influencer FLag and Unflag
@app.route("/<username>/flag/influencer/<int:influ_id>")
def flag_influencer(username,influ_id):
    influencer= Influencers.query.filter_by(influ_id=influ_id).first()
    influencer.flagged=True
    db.session.commit()
    return redirect(url_for('admin_campaigns', username=username))

@app.route("/<username>/unflag/influencer/<int:influ_id>")
def unflag_influencer(username,influ_id):
    influencer= Influencers.query.filter_by(influ_id=influ_id).first()
    influencer.flagged=False
    db.session.commit()
    return redirect(url_for('admin_profile', username=username))

#sponsor FLag and Unflag
@app.route("/<username>/flag/sponsor/<int:spon_id>")
def flag_sponsor(username,spon_id):
    sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
    sponsor.flagged=True
    db.session.commit()
    return redirect(url_for('admin_campaigns', username=username))

@app.route("/<username>/unflag/sponsor/<int:spon_id>")
def unflag_sponsor(username,spon_id):
    sponsor= Sponsors.query.filter_by(spon_id=spon_id).first()
    sponsor.flagged=False
    db.session.commit()
    return redirect(url_for('admin_profile', username=username))

#campaign FLag and Unflag
@app.route("/<username>/flag/campaign/<int:campaign_id>")
def flag_campaign(username,campaign_id):
    campaign= Campaigns.query.filter_by(campaign_id=campaign_id).first()
    campaign.flagged=True
    db.session.commit()
    return redirect(url_for('admin_campaigns', username=username))

@app.route("/<username>/unflag/campaign/<int:campaign_id>")
def unflag_campaign(username,campaign_id):
    campaign= Campaigns.query.filter_by(campaign_id=campaign_id).first()
    campaign.flagged=False
    db.session.commit()
    return redirect(url_for('admin_profile', username=username))

#Influencer Search
@app.route("/influencer/search/<int:influ_id>")
def influencer_search(influ_id):
    search_word= "%" + request.args.get("search_word")+ "%" 
    camps= Campaigns.query.filter(Campaigns.camp_search.like(search_word)).all()
    camp_summary= fetch_search_camp(camps)
    influencer= Influencers.query.filter_by(influ_id=influ_id).first()
    return render_template('user/influencer_find.html', influencer=influencer, camp=camp_summary)

# Sponsor Search

@app.route("/sponsor/search/<int:spon_id>")
def sponsor_search(spon_id):
    search_word= "%" + request.args.get("search_word")+ "%" 
    campaigns= Campaigns.query.filter(Campaigns.camp_search.like(search_word)).all()
    influencers= Influencers.query.filter(Influencers.influ_search.like(search_word)).all()
    sponsor= fetch_sponsor_camp(spon_id)
    return render_template('user/sponsor_find.html', sponsor=sponsor, campaigns=campaigns, influencers=influencers)


# Admin search
@app.route("/admin/search/<username>")
def admin_search(username):
    search_word= "%" + request.args.get("search_word")+ "%" 
    admin= Admins.query.filter_by(username=username).first()
    influencers= Influencers.query.filter(Influencers.influ_search.like(search_word)).all()
    sponsors= Sponsors.query.filter(Sponsors.spon_search.like(search_word)).all()
    camps= Campaigns.query.filter(Campaigns.camp_search.like(search_word)).all()
    camp_summary= fetch_search_camp(camps)

    return render_template('admin/admin_find.html', admin=admin, influencers=influencers, sponsors=sponsors, camp=camp_summary)


if __name__ == '__main__':
    app.run(debug=True)
