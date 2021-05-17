from flask import render_template, Blueprint, request, redirect, url_for, abort, flash, jsonify
from flask_login import current_user
from jobby.models import (
    Tasks, Bids, Users,
    WorkExperiences, Educations,
    Views, Notification, Reviews, Offers,
    Notification, TaskSkills
    )
from jobby import db, last_updated
from werkzeug.utils import secure_filename
import uuid, os, json
from utils import allowed_offer_file, get_extension, UPLOAD_OFFER_FOLDER

public = Blueprint('public',__name__)

@public.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']
        keyword = request.form['keyword']
        return redirect(url_for('.browseTasks', location=location, keyword=keyword))
    else:
        users = Users.query.filter_by(status='freelancer').all()[:5]
        featured_tasks = Tasks.query.all()[:3]
        if current_user.is_authenticated:
            return render_template('public/index.html')
        return render_template('public/index.html', users=users, featured_tasks=featured_tasks, last_updated=last_updated)
        #return render_template('public/index.html')

@public.route('/proje/<task_url>', methods=['GET', 'POST'])
def task_page(task_url):
    task_id = task_url.split('-')[-1]
    task = Tasks.query.filter_by(id=task_id).first_or_404()
    taskbids = Bids.query.filter_by(task_id=task_id).all()
    if request.method == 'GET':
        sk = TaskSkills.query.filter_by(task_id=task.id).all()
        return render_template('tasks/single-task-page.html',task=task, sk=sk, taskbids=taskbids, last_updated=last_updated)
    else:
        bid_amount = request.form['bid_amount']
        qtyInput = request.form['qtyInput']
        qtyOption = request.form['qtyOption']
        bidMessage = request.form['bidMessage']

        bid = Bids(bid_amount=bid_amount, num_delivery=qtyInput, type_delivery=qtyOption,
            message=bidMessage, user_id=current_user.id, task_id=task_id)
        notification = Notification(task_id=task_id, not_from=current_user.id, not_to=task.poster.id, not_type=1)
        task.num_bids += 1
        current_user.num_bids += 1
        db.session.add(bid)
        db.session.add(notification)
        db.session.commit()
        return jsonify({'success': True, 'msg': url_for('manage.activeBids')})

@public.route('/projects')
def browseTasks():
    tasks = Tasks.query.all()
    return render_template('public/tasks-list.html', tasks=tasks)

@public.route('/freelancer/<int:user_id>', methods=['GET', 'POST'])
def freelancer(user_id):
    #user = Users.query.filter_by(id=user_id, status='freelancer').first_or_404()
    if request.method == 'GET':
        #user.add_view()
        return render_template('public/freelancer-profile.html')
    else:
        if current_user.is_authenticated:
            offer = Offers(offered=user, offers=current_user)
            offer.subject = request.form['subject']
            offer.message = request.form['message']
            if 'file' in request.files:
                file = request.files['file']
                filename = file.filename
            if file and allowed_offer_file(filename):
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4())+get_extension(filename)
                offer.filename = unique_filename
                file.save(os.path.join(UPLOAD_OFFER_FOLDER, unique_filename))

            notif = Notification(notification_from=current_user, notification_to=user, not_type=4)
            db.session.add(offer)
            db.session.add(notif)
            db.session.commit()
            flash("Teklifiniz Başarıyla iletildi.")
            return redirect(request.url)
        else:
            flash("Teklif sunabilmek için giriş yapmalısınız!")
            return redirect(url_for('account.login'))

@public.route('/freelancers')
def browseFreelancers():
    freelancers = Users.query.filter_by(status='freelancer').all()
    return render_template('public/freelancers-list.html', freelancers=freelancers)

@public.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@public.route('/welcome')
def welcome():
    return render_template('account/welcome.html')

@public.route('/confirm')
def confirm():
    return render_template('account/email_confirmation.html')
