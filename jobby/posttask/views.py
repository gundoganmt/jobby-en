from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from jobby import db, last_updated
from jobby.models import Users, Tasks, Skills
import re, bleach

posttask = Blueprint('posttask',__name__)

@posttask.route('/posttask', methods=['GET', 'POST'])
@login_required
def post_task():
    if request.method == 'POST':
        is_form_postable = False;
        project_name = request.form["project_name"]
        location = request.form["location"]
        budget_min = request.form["budget_min"]
        budget_max = request.form["budget_max"]
        category = request.form["category"]
        description = bleach.clean(request.form["description"], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
        skills = request.form["skillsHidden"]

        #validate form
        if len(project_name) == 0:
            flash("Proje isminiz çok kısa!")
        if not category:
            flash("Lutfen bir kategori seçiniz!")
        if budget_min > budget_max:
            flash("minimum değer maximumdan fazla olamaz!")
        if not budget_min:
            budget_min = 0
        if not budget_max:
            budget_max = 0
        if len(description) < 30:
            flash("Lutfen projenizi biraz açıklayın")
        if not skills:
            flash("Lutfen en az 1 yetenek seçin!")
        if not is_form_postable and not current_user.email_approved:
            return redirect(url_for('posttask.post_task'))
        else:
            is_form_postable = True

        task = Tasks(project_name=project_name, location=location, budget_min=budget_min,
                     budget_max=budget_max, category=category, description=description, user_id=current_user.id)
        for skill in re.findall('[A-Z][^A-Z]*', skills):
            sk = Skills.query.filter_by(skill=skill).first()
            task.TSkills.append(sk)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('public.task_page', task_url=task.generate_task_link()))
    else:
        sk = Skills.query.all()
        if not current_user.email_approved:
            flash('Email adresiniz doğrulanmadı. İlan veremezsiniz!')
        return render_template('post-a-task.html', sk=sk, last_updated=last_updated)
