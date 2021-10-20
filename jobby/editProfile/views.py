from flask import render_template, Blueprint, request, flash, redirect, url_for, abort, jsonify
from flask_login import current_user, login_required
from jobby.models import Users, Skills, WorkExperiences, Educations, Categories, Countries, SkillsDb
from jobby import db, last_updated, csrf
import os, uuid, re, json, bleach
from PIL import Image
from utils import crop_max_square, allowed_img_file, get_extension, UPLOAD_IMG_FOLDER
from werkzeug.utils import secure_filename

editProfile = Blueprint('editProfile',__name__)

@editProfile.route('/editProfile/personal', methods=['POST'])
@login_required
def editProfile_personal():
    name = request.form['name']
    surname = request.form['surname']
    username = request.form['username']
    email = request.form['email']

    if len(username) < 6 or not username.isalnum():
        return jsonify({'success': False, 'msg': "You have to provide valid username."})

    if not username == current_user.username and Users.query.filter_by(username=username).first():
        return jsonify({'success': False, 'msg': "This username allready being used!"})

    if len(name) < 3 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        return jsonify({'success': False, 'msg': "The length of name and surname should be between 3 and 30"})

    if len(email) > 50 or not email:
        return jsonify({'success': False, 'msg': "Incorrect Email!"})

    if not email == current_user.email and Users.query.filter_by(email=email).first():
        return jsonify({'success': False, 'msg': "This email allready being used!"})

    current_user.name = name
    current_user.surname = surname
    current_user.username = username
    current_user.email  = email

    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        if allowed_img_file(filename):
            filename = secure_filename(filename)
            unique_filename = str(uuid.uuid4())+get_extension(filename)
            current_user.profile_picture = unique_filename
            image = Image.open(file)
            i = crop_max_square(image).resize((300, 300), Image.LANCZOS)
            i.save(os.path.join(UPLOAD_IMG_FOLDER, unique_filename), quality=95)

    db.session.commit()
    return jsonify({'success': True, 'editProfileType': "per"})

@editProfile.route('/editProfile/profile', methods=['POST'])
@login_required
def editProfile_profile():
    current_user.field_of_work = request.form['field_of_work']
    current_user.tagline = request.form['tagline']
    current_user.country = request.form['location']
    current_user.introduction = bleach.clean(request.form['introduction'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    current_user.check_status()
    db.session.commit()
    return jsonify({"success": True, "editProfileType": "p"})

@editProfile.route('/editProfile/skill', methods=['POST'])
@login_required
def editProfile_skill():
    skill = request.form['skill']
    level = request.form['level']
    if not SkillsDb.query.filter_by(skill=skill).first():
        return jsonify({"success": False, "msg": "This skill does not exist!"})
    new_skill = Skills(skill=skill, level=level, user_id=current_user.id)
    db.session.add(new_skill)
    db.session.commit()
    current_user.check_status()
    return jsonify({"success": True, "editProfileType": 's', "skill_id": new_skill.id, "skill": new_skill.skill, 'level': new_skill.level})

@editProfile.route('/editProfile/workExp', methods=['POST'])
@login_required
def editProfile_workExp():
    description = bleach.clean(request.form['desc_work'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    workExp = WorkExperiences(position=request.form['position'], company=request.form['company'], start_month=request.form['start_month_job'],
        start_year=request.form['start_year_job'], end_month=request.form['end_month_job'], end_year=request.form['end_year_job'],
        description=description, user_id=current_user.id)
    db.session.add(workExp)
    db.session.commit()
    return jsonify({"success": True, "editProfileType": 'w', 'workExp_id': workExp.id, "workExp": workExp.position, 'company': workExp.company})

@editProfile.route('/editProfile/education', methods=['POST'])
@login_required
def editProfile_education():
    description = bleach.clean(request.form['desc_edu'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    edu = Educations(field=request.form['field'], school=request.form['school'], start_month=request.form['start_month_edu'],
        start_year=request.form['start_year_edu'], end_month=request.form['end_month_edu'], end_year=request.form['end_year_edu'],
        description=description, user_id=current_user.id)
    db.session.add(edu)
    db.session.commit()
    return jsonify({"success": True, "editProfileType": 'e', "edu_id": edu.id, "field": edu.field, 'school': edu.school})

@editProfile.route('/editProfile/social', methods=['POST'])
@login_required
def editProfile_social():
    current_user.facebook = request.form['facebook']
    current_user.twitter = request.form['twitter']
    current_user.instagram = request.form['instagram']
    current_user.github = request.form['github']
    current_user.youtube = request.form['youtube']
    current_user.linkedin = request.form['linkedin']

    db.session.commit()
    return jsonify({"success": True, 'editProfileType': 'so'})

@editProfile.route('/deleteItem', methods=['POST'])
@login_required
def deleteItem():
    itemType, itemId = request.form['type_id'].split('_')
    if itemType == 'w':
        item = WorkExperiences.query.filter_by(id=itemId, user_id=current_user.id).first()
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, 'currentField': 'w'})
    elif itemType == 's':
        item = Skills.query.filter_by(id=itemId, user_id=current_user.id).first()
        db.session.delete(item)
        current_user.check_status()
        db.session.commit()
        return jsonify({"success": True, 'currentField': 's'})
    elif itemType == 'e':
        item = Educations.query.filter_by(id=itemId, user_id=current_user.id).first()
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, 'currentField': 'e'})

@editProfile.route('/editProfile')
@login_required
def editProfile_page():
    skills = Skills.query.filter_by(user_id=current_user.id).all()
    workExps = WorkExperiences.query.filter_by(Worker=current_user).all()
    categories = Categories.query.all()
    locations = Countries.query.all()
    sks = SkillsDb.query.all()
    edus = Educations.query.filter_by(student=current_user).all()
    return render_template('editProfile/editProfile.html', last_updated=last_updated, skills=skills,
        workExps=workExps, edus=edus, categories=categories, locations=locations, sks=sks)

@editProfile.app_errorhandler(413)
def file_too_large(e):
    flash('The file size is too big! At most 2Mb.')
    return redirect(request.url)
