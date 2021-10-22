from flask import render_template, Blueprint, request, url_for, jsonify, redirect, flash, abort, current_app, send_file
from jobby.models import (Bids, Tasks, Users, Views, Notification, Countries, SkillsDb, MailConfig, Admin,
    Reviews, Offers, Messages, Categories, Skills, WorkExperiences, Educations, TaskSkills, SiteSettings)
from jobby import db
from PIL import Image
from datetime import datetime, timedelta
from utils import (crop_max_square, allowed_img_file, get_extension,
    UPLOAD_IMG_FOLDER, UPLOAD_TASK_FOLDER, allowed_offer_file, UPLOAD_OFFER_FOLDER)
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os, uuid
from flask_login import current_user
from utils import admin_required

admin = Blueprint('admin',__name__)

@admin.route('/adminpanel')
@admin_required()
def adminpanel():
    total_two_months = db.session.query(Users).filter(Users.member_since > datetime.now()-timedelta(60)).count()
    total_new_users = db.session.query(Users).filter(Users.member_since > datetime.now()-timedelta(30))

    total_two_weeks = db.session.query(Users).filter(Users.member_since > datetime.now()-timedelta(14)).count()
    week_new_users = db.session.query(Users).filter(Users.member_since > datetime.now()-timedelta(7))

    last_month = total_two_months - total_new_users.count()
    last_week = total_two_weeks - week_new_users.count()
    all_users = Users.query.all()

    if not last_month==0:
        rate_month = 100*(total_new_users.count()-last_month)/last_month
    else:
        rate_month=0.0
    if not last_week==0:
        rate_week = 100*(week_new_users.count()-last_week)/last_week
    else:
        rate_week=0.0

    total_two_months_pro = db.session.query(Tasks).filter(Tasks.time_posted > datetime.now()-timedelta(60)).count()
    total_new_pro = db.session.query(Tasks).filter(Tasks.time_posted > datetime.now()-timedelta(30))

    total_two_weeks_pro = db.session.query(Tasks).filter(Tasks.time_posted > datetime.now()-timedelta(14)).count()
    week_new_pro = db.session.query(Tasks).filter(Tasks.time_posted > datetime.now()-timedelta(7))

    last_month_pro = total_two_months_pro - total_new_pro.count()
    last_week_pro = total_two_weeks_pro - week_new_pro.count()
    all_pro = Tasks.query.all()

    if not last_month_pro==0:
        rate_month_pro = 100*(total_new_pro.count()-last_month_pro)/last_month_pro
    else:
        rate_month_pro=0.0
    if not last_week_pro==0:
        rate_week_pro = 100*(week_new_pro.count()-last_week_pro)/last_week_pro
    else:
        rate_week_pro=0.0

    return render_template('admin/index.html', rate_month=rate_month, rate_month_pro=rate_month_pro,
        all_users=all_users, week_new_users=week_new_users.all(), rate_week=rate_week, all_pro=all_pro,
        week_new_pro=week_new_pro.all(), rate_week_pro=rate_week_pro)

@admin.route('/adminpanel/search', methods=['GET', 'POST'])
@admin_required()
def search():
    if request.method == 'GET':
        keyword = request.args.get('kw', type=str)
        if keyword:
            projects = Tasks.query.whoosh_search(keyword).all()
            users = Users.query.whoosh_search(keyword).all()

        return render_template('admin/search.html', users=users, projects=projects)
    else:
        keyword = request.form['keyword']
        return redirect(url_for('.search', kw=keyword))

@admin.route('/adminpanel/<table>', methods=['GET', 'POST'])
@admin_required()
def dbop(table):
    if table == 'users':
        users = Users.query.all()
        return render_template('admin/usersTable.html', users=users)
    elif table == 'projects':
        projects = Tasks.query.all()
        return render_template('admin/projectsTable.html', projects=projects)
    elif table == 'site-settings':
        mail_config = db.session.query(MailConfig).first()
        ss = db.session.query(SiteSettings).first()
        admins = Admin.query.all()
        return render_template('admin/site-settings.html', admins=admins, ss=ss, mail_config=mail_config)
    elif table == 'bids':
        bids = Bids.query.all()
        return render_template('admin/bidsTable.html', bids=bids)
    elif table == 'offers':
        offers = Offers.query.all()
        return render_template('admin/offersTable.html', offers=offers)
    elif table == "messages":
        msgs = Messages.query.all()
        return render_template('admin/messagesTable.html', msgs=msgs)
    elif table == 'reviews':
        rws = Reviews.query.all()
        return render_template('admin/reviewsTable.html', rws=rws)

@admin.route('/adminpanel/create/<table>', methods=['GET', 'POST'])
@admin_required()
def create(table):
    if request.method == 'GET':
        if table == 'messages':
            users = Users.query.all()
            return render_template('admin/createMessage.html', users=users)
        elif table == 'users':
            return render_template('admin/createUser.html')
        elif table == 'categories':
            cats = Categories.query.all()
            return render_template('admin/createCategories.html', cats=cats)
        elif table == 'countries':
            ctr = Countries.query.all()
            return render_template('admin/createCountries.html', ctr=ctr)
        elif table == 'skills':
            sks = SkillsDb.query.all()
            return render_template('admin/createSkills.html', sks=sks)
        elif table == 'bids':
            users = Users.query.filter_by(status='freelancer').all()
            projects = Tasks.query.all()
            return render_template('admin/createBids.html', users=users, projects=projects)
        elif table == 'reviews':
            users = Users.query.filter_by(status='freelancer').all()
            projects = Tasks.query.all()
            return render_template('admin/createReviews.html', users=users, projects=projects)
        elif table == 'offers':
            users = Users.query.all()
            projects = Tasks.query.all()
            return render_template('admin/createOffers.html', users=users, projects=projects)
        elif table == 'projects':
            ctrs = Categories.query.all()
            lcts = Countries.query.all()
            sks = SkillsDb.query.all()
            users = Users.query.all()
            return render_template('admin/createProjects.html', ctrs=ctrs, lcts=lcts, sks=sks, users=users)
        else:
            return abort(404), 404
    else:
        if table == 'messages':
            body = request.form['MessageBody']
            sender = Users.query.filter_by(username=request.form['MessageSender']).first()
            recipient = Users.query.filter_by(username=request.form['MessageRecipient']).first()

            if sender == recipient:
                flash("Sender and recipient cannot be same!", "error")
                return redirect(request.url)

            if not sender:
                flash("Sender Not found!", "error")
                return redirect(request.url)
            if not recipient:
                flash("Recipient Not found!", "error")
                return redirect(request.url)
            msg = Messages(sender=sender, recipient=recipient, body=body)

            db.session.add(msg)
            db.session.commit()
            flash("Message Successfully Created!", "success")
            return redirect(request.url)

        elif table == 'categories':
            if current_user.username == 'gundoganm':
                category = request.form['category']
                if len(category) < 3 or len(category) > 150:
                    flash('Category length should be between 3 and 150')
                    return redirect(request.url)
                cat = Categories(category=category)
                if 'file' in request.files:
                    file = request.files['file']
                    filename = file.filename
                    if allowed_img_file(filename):
                        filename = secure_filename(filename)
                        unique_filename = str(uuid.uuid4())+get_extension(filename)
                        cat.cat_pic = unique_filename
                        file.save(os.path.join(UPLOAD_IMG_FOLDER, unique_filename))
                        db.session.add(cat)
                        db.session.commit()
                        return redirect(request.url)
                    else:
                        flash("Not allowed file type. Only jpeg, png or jpg")
                        return redirect(request.url)
                else:
                    flash("İmage is required")
                    return redirect(request.url)
            else:
                flash("Category creation is not allowed for demo accounts!")
                return redirect(request.url)
        elif table == 'countries':
            country = request.form['country']
            if len(country) < 2 or len(country) > 100:
                flash("Country length should be between 2 and 100")
                return redirect(request.url)
            if Countries.query.filter_by(country=country).first():
                flash("Location already exist")
                return redirect(request.url)
            ctr = Countries(country=country)
            db.session.add(ctr)
            db.session.commit()
            return redirect(request.url)
        elif table == 'skills':
            skill = request.form['skill']
            if len(skill) == 0 or len(skill) > 100:
                flash("skill length should be between 0 and 100")
                return redirect(request.url)
            if SkillsDb.query.filter_by(skill=skill).first():
                flash("This skill already exist!")
                return redirect(request.url)
            sk = SkillsDb(skill=skill)
            db.session.add(sk)
            db.session.commit()
            return redirect(request.url)
        elif table == 'projects':
            project_name = request.form["project_name"].capitalize()
            location = request.form["location"]
            budget_min = request.form["budget_min"] or 0
            budget_max = request.form["budget_max"] or 0
            category = request.form["category"]
            skills_list = request.form.getlist('skills')
            description = request.form["description"]
            poster = Users.query.filter_by(username=request.form['poster']).first()
            if not poster:
                flash("There is an error about project poster. Try again!", 'error')
                return redirect(request.url)

            if int(budget_min) > int(budget_max):
                flash("Budget min cannot exceed budget max. Try again!", 'error')
                return redirect(request.url)

            task = Tasks(project_name=project_name, location=location, budget_min=budget_min, time_posted=datetime.now(),
                         is_active=True, budget_max=budget_max, category=category, description=description, user_id=poster.id)

            if 'file' in request.files:
                file = request.files['file']
                filename = file.filename
                if allowed_img_file(filename):
                    filename = secure_filename(filename)
                    unique_filename = str(uuid.uuid4())+get_extension(filename)
                    task.task_pic = unique_filename
                    image = Image.open(file)
                    i = crop_max_square(image).resize((356, 200), Image.LANCZOS)
                    i.save(os.path.join(UPLOAD_TASK_FOLDER, unique_filename), quality=95)
                else:
                    flash('Allowed image files jpeg, png, jpg', 'error')
                    return redirect(request.url)

            db.session.add(task)
            db.session.commit()

            for skill in skills_list:
                tskills = TaskSkills(skill=skill, task_id=task.id)
                db.session.add(tskills)
            db.session.commit()
            flash("Project Successfully Created!", 'success')
            return redirect(request.url)
        elif table == 'bids':
            bid_amount = request.form['bid_amount']
            qtyInput = request.form['qtyInput']
            qtyOption = request.form['qtyOption']
            BidMessage = request.form['BidMessage']
            bidder = Users.query.filter_by(username=request.form['ProjectBidder']).first()
            bidded = Tasks.query.get(request.form['BiddedProject'])

            if not bidder:
                flash("User Not found!", "error")
                return redirect(request.url)
            if not bidded:
                flash("Project Not found!", "error")
                return redirect(request.url)
            if not bidded.poster == bidder:
                flash("Bidder cannot be project poster! Choose other bidder.", "error")
                return redirect(request.url)

            bid = Bids(bid_amount=bid_amount, num_delivery=qtyInput, type_delivery=qtyOption,
                message=BidMessage, user_id=bidder.id, task_id=bidded.id)
            notification = Notification(task_id=bidded.id, not_from=bidder.id, not_to=bidded.poster.id, not_type=1)
            bidded.num_bids += 1
            bidder.num_bids += 1
            db.session.add(bid)
            db.session.add(notification)
            db.session.commit()
            flash("Bid Successfully Created", "success")
            return redirect(request.url)
        elif table == 'reviews':
            reviewFree = Users.query.filter_by(username=request.form['reviewFree']).first()
            reviewProject = Tasks.query.get(request.form['reviewProject'])
            body = request.form['reviewMessage']
            rating = request.form['rating']
            recom = request.form['recom'] == 'yes'
            in_time = request.form['intime'] == 'yes'

            if int(rating) < 1 or int(rating) > 5:
                flash('invalid rating!', 'error')
                return redirect(request.url)

            rv = Reviews(recommendation=recom, in_time=in_time, body=body, rating=float(rating),
                task_id=reviewProject.id, freelancer=reviewFree.id, employer=reviewProject.poster.id)

            notif = Notification(notification_to=rv.reviewed_pro, notification_from=rv.reviewed_emp, notedTask=rv.reviewed, not_type=5)

            db.session.add(notif)
            db.session.add(rv)
            db.session.commit()
            rv.reviewed_pro.addRating(float(rating))
            flash('Review succesfully created!', 'success')
            return redirect(request.url)
        elif table == 'offers':
            subject = request.form['subject']
            offeredTask = Tasks.query.get(request.form['offered_project'])
            message = request.form['message']
            offers = Users.query.filter_by(username=request.form['offerer']).first()
            offered = Users.query.filter_by(username=request.form['offered']).first()

            if offers == offered:
                flash("Offerer and Offered cannot be same!", "error")
                return redirect(request.url)

            offer = Offers(offered=offered, offers=offers, offeredTask=offeredTask, subject=subject, message=message)

            if 'file' in request.files:
                file = request.files['file']
                filename = file.filename
                if allowed_offer_file(filename):
                    filename = secure_filename(filename)
                    unique_filename = str(uuid.uuid4())+get_extension(filename)
                    offer.filename = unique_filename
                    file.save(os.path.join(UPLOAD_OFFER_FOLDER, unique_filename))
                else:
                    if filename:
                        flash("Not allowed file type! 'docx', 'doc', 'pdf', 'jpeg', 'jpg', 'png' required", "error")
                        return redirect(request.url)

            notif = Notification(notification_from=offers, notification_to=offered, not_type=4)
            db.session.add(offer)
            db.session.add(notif)
            db.session.commit()
            flash('Offer succesfully Created!', "success")
            return redirect(request.url)
        elif table == 'emailSettings':
            provider = request.form['ServisProvider']
            mail_server = request.form['MailServer']
            port = request.form['port']
            use_TLS = request.form['UseTLS'] == 'Yes'
            use_SSL = request.form['UseSSL'] == 'Yes'
            username = request.form['username']
            password = request.form['password']

            config = db.session.query(MailConfig).first()
            if not config:
                config = MailConfig(provider=provider, mail_server=mail_server, use_SSL=use_SSL,
                    port=port, use_TLS=use_TLS, username=username, password=password)

                db.session.add(config)
                db.session.commit()
            else:
                config.provider = provider
                config.mail_server = mail_server
                config.use_SSL = use_SSL
                config.use_TLS = use_TLS
                config.port = port
                config.username = username
                config.password = password

                db.session.commit()

            app = current_app._get_current_object()
            app.config.update(
                MAIL_SERVER=mail_server,
                MAIL_PORT=port,
                MAIL_USE_TLS = use_TLS,
                MAIL_USE_SSL = use_SSL,
                MAIL_USERNAME = username,
                MAIL_PASSWORD = password
            )

            flash("Record Updated Successfully!", "success")
            return redirect(url_for('.dbop', table='site-settings'))
        elif table == 'admin':
            full_name = request.form['full_name']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            if len(username) < 3 or not username.isalnum():
                return jsonify({'success': False, 'msg': "You have to provide valid username."})

            if Admin.query.filter_by(username=username).first():
                return jsonify({'success': False, 'msg': "This username allready being used!"})

            if len(password) < 6:
                return jsonify({'success': False, 'msg': "You have to provide valid password. At least 6 character"})

            if len(email) > 50:
                return jsonify({'success': False, 'msg': "Incorrect Email!"})

            if Admin.query.filter_by(email=email).first():
                return jsonify({'success': False, 'msg': "This email allready being used!"})

            admin = Admin(username=username, email=email, password=generate_password_hash(password, method='sha256'),
                full_name=full_name)

            if 'file' in request.files:
                file = request.files['file']
                filename = file.filename
                if allowed_img_file(filename):
                    filename = secure_filename(filename)
                    unique_filename = str(uuid.uuid4())+get_extension(filename)
                    admin.profile_picture = unique_filename
                    image = Image.open(file)
                    i = crop_max_square(image).resize((300, 300), Image.LANCZOS)
                    i.save(os.path.join(UPLOAD_IMG_FOLDER, unique_filename), quality=95)

            db.session.add(admin)
            db.session.commit()
            return jsonify({'success': True, 'admin_id': admin.id})
        elif table == 'SiteSocial':
            facebook = request.form['facebook']
            twitter = request.form['twitter']
            instagram = request.form['instagram']
            github = request.form['github']
            youtube = request.form['youtube']
            linkedin = request.form['linkedin']

            ss = db.session.query(SiteSettings).first()
            if not ss:
                ss = SiteSettings(facebook=facebook, twitter=twitter, instagram=instagram,
                    github=github, youtube=youtube, linkedin=linkedin)
                db.session.add(ss)
                db.session.commit()
                return jsonify({"success": True})
            else:
                ss.facebook = facebook
                ss.twitter = twitter
                ss.instagram = instagram
                ss.github = github
                ss.youtube = youtube
                ss.linkedin = linkedin

                db.session.commit()
                return jsonify({"success": True})

@admin.route('/adminpanel/chart/<view_type>')
@admin_required()
def views(view_type):
    if view_type == 'users':
        users = Users.query.filter_by(status='freelancer').all()
        return render_template('admin/views.html', users=users)
    elif view_type == 'projects':
        projects = Tasks.query.all()
        return render_template('admin/views.html', projects=projects)

@admin.route('/user-view-data/<username>')
@admin_required()
def userViewData(username):
    user = Users.query.filter_by(username=username).first()
    views = Views.query.filter_by(user_id=user.id).first()
    view_list = [views.monday, views.tuesday, views.wednesday, views.thursday,
        views.friday, views.saturday, views.sunday]
    return jsonify({'success': True, 'view_list': view_list})

@admin.route('/project-view-data/<pro_id>')
@admin_required()
def projectViewData(pro_id):
    project = Tasks.query.get(pro_id)
    views = Views.query.filter_by(task_id=project.id).first()
    view_list = [views.monday, views.tuesday, views.wednesday, views.thursday,
        views.friday, views.saturday, views.sunday]
    return jsonify({'success': True, 'view_list': view_list})

@admin.route('/createUser', methods=['POST'])
@admin_required()
def createUser():
    name = request.form['name']
    surname = request.form['surname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phone_number = request.form['phone']

    if len(username) < 6 or not username.isalnum():
        flash("You have to provide valid username.")
        return redirect(url_for('.create', table='users'))

    if Users.query.filter_by(username=username).first():
        flash("This username allready being used!")
        return redirect(url_for('.create', table='users'))

    if len(password) < 6:
        flash("You have to provide valid password. At least 6 character")
        return redirect(url_for('.create', table='users'))

    if len(name) < 3 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        flash("The length of name and surname should be between 3 and 30")
        return redirect(url_for('.create', table='users'))

    if len(email) > 50:
        flash("Incorrect Email!")
        return redirect(url_for('.create', table='users'))

    if Users.query.filter_by(email=email).first():
        flash("This email allready being used!")
        return redirect(url_for('.create', table='users'))

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = Users(username=username, name=name, surname=surname, email=email, phone_number=phone_number,
        password=hashed_password, member_since=datetime.utcnow(), status='employer', email_approved=True)

    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        if allowed_img_file(filename):
            filename = secure_filename(filename)
            unique_filename = str(uuid.uuid4())+get_extension(filename)
            new_user.profile_picture = unique_filename
            image = Image.open(file)
            i = crop_max_square(image).resize((300, 300), Image.LANCZOS)
            i.save(os.path.join(UPLOAD_IMG_FOLDER, unique_filename), quality=95)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('.editUser', user_id=new_user.id))

@admin.route('/adminpanel/editMessage/<int:ms_id>', methods=['GET', 'POST'])
@admin_required()
def editMessage(ms_id):
    msg = Messages.query.get(ms_id)
    if request.method == 'GET':
        users = Users.query.all()
        return render_template('admin/editMessage.html', msg=msg, users=users)
    else:
        body = request.form['MessageBody']
        sender = Users.query.filter_by(username=request.form['MessageSender']).first()
        recipient = Users.query.filter_by(username=request.form['MessageRecipient']).first()

        if sender == recipient:
            flash("Sender and recipient cannot be same!", "error")
            return redirect(request.url)

        if not sender:
            flash("Sender Not found!", "error")
            return redirect(request.url)
        if not recipient:
            flash("Recipient Not found!", "error")
            return redirect(request.url)

        msg.sender = sender
        msg.recipient = recipient
        msg.body = body

        db.session.commit()
        flash("Message Successfully Edited!", "success")
        return redirect(request.url)

@admin.route('/adminpanel/editUser/<int:user_id>')
@admin_required()
def editUser(user_id):
    if request.method == 'GET':
        user = Users.query.get(user_id)
        fr = request.args.get('from', type=str)
        cats = Categories.query.all()
        lcts = Countries.query.all()
        sks = SkillsDb.query.all()
        if fr:
            return render_template('admin/editUser.html', user=user, fr=fr, cats=cats, lcts=lcts, sks=sks)

        return render_template('admin/editUser.html', user=user, fr=fr, cats=cats, lcts=lcts, sks=sks)

@admin.route('/adminpanel/editReview/<int:rv_id>', methods=['GET', 'POST'])
@admin_required()
def editReview(rv_id):
    rv = Reviews.query.get(rv_id)
    if request.method == 'GET':
        users = Users.query.filter_by(status='freelancer').all()
        projects = Tasks.query.all()
        return render_template('admin/editReviews.html', users=users, projects=projects, rv=rv)
    else:
        reviewFree = Users.query.filter_by(username=request.form['reviewFree']).first()
        reviewProject = Tasks.query.get(request.form['reviewProject'])
        body = request.form['reviewMessage']
        rating = request.form['rating']
        recom = request.form['recom'] == 'yes'
        in_time = request.form['intime'] == 'yes'
        old_rating = rv.rating

        if int(rating) < 1 or int(rating) > 5:
            flash('invalid rating!', 'error')
            return redirect(request.url)

        rv.recommendation = recom
        rv.in_time = in_time
        rv.body = body
        rv.rating = float(rating)
        rv.task_id = reviewProject.id
        rv.freelancer = reviewFree.id
        rv.employer = reviewProject.poster.id

        db.session.commit()
        rv.reviewed_pro.editRating(old_rating, float(rating))
        flash('Review succesfully edited!', 'success')
        return redirect(request.url)

@admin.route('/adminpanel/editBid/<int:bid_id>', methods=['GET', 'POST'])
@admin_required()
def editBid(bid_id):
    bid = Bids.query.get(bid_id)
    if request.method == 'GET':
        users = Users.query.filter_by(status='freelancer').all()
        projects = Tasks.query.all()
        return render_template('admin/editBid.html', bid=bid, users=users, projects=projects)
    else:
        bid_amount = request.form['bid_amount']
        qtyInput = request.form['qtyInput']
        qtyOption = request.form['qtyOption']
        BidMessage = request.form['BidMessage']
        bidder = Users.query.filter_by(username=request.form['ProjectBidder']).first()
        bidded = Tasks.query.get(request.form['BiddedProject'])

        if not bidder:
            flash("User Not found!", "error")
            return redirect(request.url)
        if not bidded:
            flash("Project Not found!", "error")
            return redirect(request.url)

        bid.bid_amount = bid_amount
        bid.num_delivery = qtyInput
        bid.type_delivery = qtyOption
        bid.message = BidMessage
        bid.bidder = bidder
        bid.bidded = bidded

        db.session.commit()
        flash("Bid Successfully Edited", "success")
        return redirect(request.url)

@admin.route('/adminpanel/editOffer/<int:offer_id>', methods=['GET', 'POST'])
@admin_required()
def editOffer(offer_id):
    offer = Offers.query.get(offer_id)
    if request.method == 'GET':
        users = Users.query.all()
        projects = Tasks.query.all()
        return render_template('admin/editOffer.html', offer=offer, users=users, projects=projects)
    else:
        subject = request.form['subject']
        offeredTask = Tasks.query.get(request.form['offered_project'])
        message = request.form['message']
        offers = Users.query.filter_by(username=request.form['offerer']).first()
        offered = Users.query.filter_by(username=request.form['offered']).first()

        if offers == offered:
            flash("Offerer and Offered cannot be same!", "error")
            return redirect(request.url)

        offer.offered = offered
        offer.offers = offers
        offer.offeredTask = offeredTask
        offer.subject = subject
        offer.message = message

        if 'file' in request.files:
            file = request.files['file']
            filename = file.filename
            if allowed_offer_file(filename):
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4())+get_extension(filename)
                os.remove(os.path.join(UPLOAD_OFFER_FOLDER, offer.filename))
                offer.filename = unique_filename
                file.save(os.path.join(UPLOAD_OFFER_FOLDER, unique_filename))
            else:
                if filename:
                    flash("Not allowed file type! 'docx', 'doc', 'pdf', 'jpeg', 'jpg', 'png' required", "error")
                    return redirect(request.url)

        db.session.commit()
        flash('Offer succesfully edited!', "success")
        return redirect(request.url)

@admin.route('/adminpanel/editProject/<int:pro_id>', methods=['GET', 'POST'])
@admin_required()
def editProject(pro_id):
    project = Tasks.query.get(pro_id)
    if request.method == 'GET':
        pro_skills = []
        views = Views.query.filter_by(viewedTask=project).first()
        sks = SkillsDb.query.all()
        cats = Categories.query.all()
        lcts = Countries.query.all()
        for s in TaskSkills.query.filter_by(task_id=project.id).all():
            pro_skills.append(s.skill)
        users = Users.query.all()
        return render_template('admin/editProject.html', project=project, views=views,
            sks=sks, pro_skills=pro_skills, users=users, cats=cats, lcts=lcts)
    else:
        project_name = request.form["project_name"].capitalize()
        location = request.form["location"]
        budget_min = request.form["budget_min"] or 0
        budget_max = request.form["budget_max"] or 0
        category = request.form["category"]
        skills_list = request.form.getlist('skills')
        description = request.form["description"]
        poster = Users.query.filter_by(username=request.form['poster']).first()

        if not poster:
            flash("There is an error about project poster. Try again!", 'error')
            return redirect(request.url)

        if budget_min > budget_max:
            flash("Budget min cannot exceed budget max. Try again!", 'error')
            return redirect(request.url)

        project.project_name = project_name
        project.location = location
        project.budget_min = budget_min
        project.budget_max = budget_max
        project.category = category
        project.description = description
        project.poster = poster
        project.time_posted = datetime.now()
        project.is_active = True

        if 'file' in request.files:
            file = request.files['file']
            filename = file.filename
            if allowed_img_file(filename):
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4())+get_extension(filename)
                os.remove(os.path.join(UPLOAD_TASK_FOLDER, project.task_pic))
                project.task_pic = unique_filename
                image = Image.open(file)
                i = crop_max_square(image).resize((356, 200), Image.LANCZOS)
                i.save(os.path.join(UPLOAD_TASK_FOLDER, unique_filename), quality=95)

        db.session.commit()

        for skill in skills_list:
            is_exist = TaskSkills.query.filter_by(skill=skill, task_id=project.id).first()
            if not is_exist:
                t = TaskSkills(skill=skill, task_id=project.id)
                db.session.add(t)
        db.session.commit()

        flash("Project Successfully Created!", 'success')
        return redirect(request.url)

@admin.route('/editUser/personel/<int:user_id>', methods=['POST'])
@admin_required()
def personel(user_id):
    name = request.form['name']
    surname = request.form['surname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phone_number = request.form['phone']

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'msg': "Error occured refresh the page please!"})

    if len(username) < 6 or not username.isalnum():
        return jsonify({'success': False, 'msg': "You have to provide valid username."})

    if not username == user.username and Users.query.filter_by(username=username).first():
        return jsonify({'success': False, 'msg': "This username allready being used!"})

    if len(password) < 6:
        return jsonify({'success': False, 'msg': "You have to provide valid password. At least 6 character"})

    if len(name) < 3 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        return jsonify({'success': False, 'msg': "The length of name and surname should be between 3 and 30"})

    if len(email) > 50 or not email:
        return jsonify({'success': False, 'msg': "Incorrect Email!"})

    if not email == user.email and Users.query.filter_by(email=email).first():
        return jsonify({'success': False, 'msg': "This email allready being used!"})

    user.name = name
    user.surname = surname
    user.username = username
    user.email  = email
    user.phone_number = phone_number
    if not password == user.password:
        user.password = generate_password_hash(password, method='sha256')

    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        if allowed_img_file(filename):
            filename = secure_filename(filename)
            unique_filename = str(uuid.uuid4())+get_extension(filename)
            user.profile_picture = unique_filename
            image = Image.open(file)
            i = crop_max_square(image).resize((300, 300), Image.LANCZOS)
            i.save(os.path.join(UPLOAD_IMG_FOLDER, unique_filename), quality=95)

    db.session.commit()
    return jsonify({'success': True, 'editProfileType': "p"})

@admin.route('/editUser/profile/<int:user_id>', methods=['POST'])
@admin_required()
def profile(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'success': False, "msg": 'Error occured. Refresh the page please!'})
    user.field_of_work = request.form['field_of_work']
    user.tagline = request.form['tagline']
    user.country = request.form['country']
    user.introduction = request.form['introduction']
    user.check_status()
    db.session.commit()
    return jsonify({'success': True, "editProfileType": 'pro'})

@admin.route('/editUser/skill/<int:user_id>', methods=['POST'])
@admin_required()
def skill(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'success': False, "msg": 'Error occured. Refresh the page please!'})
    skill = request.form['skill']
    level = request.form['level']
    sk = Skills.query.filter_by(skill=skill, user_id=user.id).first()
    if sk:
        return jsonify({'success': False, "msg": 'This skill allready exist!'})
    sk = Skills(skill=skill, level=level, user_id=user.id)
    db.session.add(sk)
    db.session.commit()
    user.check_status()
    return jsonify({'success': True, "editProfileType": 's', "skill": skill, "level": level, "skill_id": sk.id})

@admin.route('/editUser/social/<user_id>', methods=['POST'])
@admin_required()
def social(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'success': False, "msg": 'Error occured. Refresh the page please!'})

    user.facebook = request.form['facebook']
    user.twitter = request.form['twitter']
    user.instagram = request.form['instagram']
    user.github = request.form['github']
    user.youtube = request.form['youtube']
    user.linkedin = request.form['linkedin']

    db.session.commit()

    return jsonify({"success": True, 'editProfileType': 'so'})

@admin.route('/editUser/workexp/<user_id>', methods=['POST'])
@admin_required()
def workexp(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'success': False, "msg": 'Error occured. Refresh the page please!'})

    position = request.form['position']
    company = request.form['company']
    start_month = request.form['start_month_job']
    start_year = request.form['start_year_job']
    end_month = request.form['end_month_job']
    end_year = request.form['end_year_job']
    description = request.form['desc_work']

    workexp = WorkExperiences(position=position, company=company, start_month=start_month, start_year=start_year,
        end_month=end_month, end_year=end_year, description=description, user_id=user.id)
    db.session.add(workexp)
    db.session.commit()

    return jsonify({"success": True, "position": position, "company": company,
        "workExp_id": workexp.id, 'editProfileType': 'w', "duration": workexp.start_month + " " + str(workexp.start_year) + " - " + workexp.end_month + " " + str(workexp.end_year)})

@admin.route('/editUser/education/<user_id>', methods=['POST'])
@admin_required()
def education(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'success': False, "msg": 'Error occured. Refresh the page please!'})

    field = request.form['field']
    school = request.form['school']
    start_month = request.form['start_month_edu']
    start_year = request.form['start_year_edu']
    end_month = request.form['end_month_edu']
    end_year = request.form['end_year_edu']
    description = request.form['desc_edu']

    edu = Educations(field=field, school=school, start_month=start_month, start_year=start_year,
        end_month=end_month, end_year=end_year, description=description, user_id=user.id)
    db.session.add(edu)
    db.session.commit()

    return jsonify({"success": True, "field": field, "school": school, "edu_id": edu.id, 'editProfileType': 'e',
        "duration": edu.start_month + " " + str(edu.start_year) + " - " + edu.end_month + " " + str(edu.end_year)})

@admin.route('/deleteItem/<type_id>')
@admin_required()
def deleteItem(type_id):
    itemType, itemId = type_id.split('_')
    if itemType == 'w':
        item = WorkExperiences.query.get(itemId)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, 'currentField': 'w'})
    elif itemType == 's':
        item = Skills.query.get(itemId)
        db.session.delete(item)
        item.skilled.check_status()
        db.session.commit()
        return jsonify({"success": True, 'currentField': 's'})
    elif itemType == 'e':
        item = Educations.query.get(itemId)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, 'currentField': 'e'})
    elif itemType == 'ad':
        if current_user.username =='admin':
            return jsonify({'success': False, "msg": "Cannot delete this admin!"})

        adm = Admin.query.get(itemId)
        if adm:
            db.session.delete(adm)
            db.session.commit()
            if adm.profile_picture:
                os.remove(os.path.join(UPLOAD_IMG_FOLDER, adm.profile_picture))
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, "msg": "Something bad happened! Refresh the page and try again!"})
    elif itemType == 'cat':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        cat = Categories.query.get(itemId)
        if cat:
            db.session.delete(cat)
            db.session.commit()
            os.remove(os.path.join(UPLOAD_IMG_FOLDER, cat.cat_pic))
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, "msg": "Something bad happened please refresh the page!"})
    elif itemType == 'ctr':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        ctr = Countries.query.get(itemId)
        if ctr:
            db.session.delete(ctr)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, "msg": "Something bad happened please refresh the page!"})
    elif itemType == 'sk':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        sk = SkillsDb.query.get(itemId)
        if sk:
            db.session.delete(sk)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, "msg": "Something bad happened please refresh the page!"})
    elif itemType == 'u':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        user = Users.query.get(itemId)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    elif itemType == 'pr':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        pr = Tasks.query.get(itemId)
        db.session.delete(pr)
        db.session.commit()
        return jsonify({'success': True})
    elif itemType == 'b':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        b = Bids.query.get(itemId)
        db.session.delete(b)
        db.session.commit()
        return jsonify({'success': True})
    elif itemType == 'o':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        o = Offers.query.get(itemId)
        if o.filename:
            os.remove(os.path.join(UPLOAD_OFFER_FOLDER, o.filename))
        db.session.delete(o)
        db.session.commit()
        return jsonify({'success': True})
    elif itemType == 'm':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        m = Messages.query.get(itemId)
        db.session.delete(m)
        db.session.commit()
        return jsonify({'success': True})
    elif itemType == 'rv':
        if current_user.username == 'admin':
            return jsonify({'success': True, "msg": "Record did NOT actually deleted!"})

        rv = Reviews.query.get(itemId)
        db.session.delete(rv)
        db.session.commit()
        return jsonify({'success': True})

@admin.route('/download/<filename>')
@admin_required()
def download(filename):
    path = os.path.join(UPLOAD_OFFER_FOLDER, filename)
    return send_file(path, as_attachment=True)
