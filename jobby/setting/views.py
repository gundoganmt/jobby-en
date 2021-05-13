from flask import render_template, Blueprint, request, flash, redirect, url_for, abort, jsonify
from flask_login import current_user, login_required
from jobby.models import Users, Skills, WorkExperiences, Educations
from jobby import db, last_updated, csrf
import os, uuid, re, json, bleach
from PIL import Image
from utils import crop_max_square, allowed_img_file, get_extension, UPLOAD_IMG_FOLDER
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

setting = Blueprint('setting',__name__)

@setting.route('/setting', methods=['POST'])
@login_required
def setting_personel():
    if not request.form['name'] or not request.form['surname']:
        flash('İsim veya soyisim boş olamaz')
        return redirect(request.url)
    else:
        current_user.name = request.form['name']
        current_user.surname = request.form['surname']

    current_user.email = request.form['email']
    current_user.phone_number = request.form['phone_number']

    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
    if file and allowed_img_file(filename):
        filename = secure_filename(filename)
        unique_filename = str(uuid.uuid4())+get_extension(filename)
        current_user.profile_picture = unique_filename
        image = Image.open(file)
        i = crop_max_square(image).resize((300, 300), Image.LANCZOS)
        i.save(os.path.join(UPLOAD_IMG_FOLDER, unique_filename), quality=95)
    db.session.commit()
    return redirect(request.url)

@setting.route('/setting/profile', methods=['POST'])
@login_required
def setting_profile():
    data = request.get_json(force=True)
    current_user.field_of_work = data['field_of_work']
    current_user.tagline = data['tagline']
    current_user.province = data['province']
    current_user.introduction = bleach.clean(data['introduction'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    current_user.check_status()
    db.session.commit()
    return jsonify({"success": True, "settingType": "p", "msg": "Profil ayarlarınız değişti."})

@setting.route('/setting/skill', methods=['POST'])
@login_required
def setting_skill():
    data = request.get_json(force=True)
    skill = Skills.query.filter_by(skill=data['skill']).first()
    skill.level = data['level']
    current_user.UserSkills.append(skill)
    current_user.check_status()
    db.session.commit()
    return jsonify({"success": True, "settingType": 's', "skill_id": skill.id, "skill": skill.skill})

@setting.route('/setting/workExp', methods=['POST'])
@login_required
def setting_workExp():
    data = request.get_json(force=True)
    description = bleach.clean(data['desc_work'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    workExp = WorkExperiences(position=data['position'], company=data['company'], start_month=data['start_month_job'],
        start_year=data['start_year_job'], end_month=data['end_month_job'], end_year=data['end_year_job'],
        description=description, user_id=current_user.id)
    db.session.add(workExp)
    db.session.commit()
    return jsonify({"success": True, "settingType": 'w', 'workExp_id': workExp.id, "workExp": workExp.position})

@setting.route('/setting/education', methods=['POST'])
@login_required
def setting_education():
    data = request.get_json(force=True)
    description = bleach.clean(data['desc_edu'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    edu = Educations(field=data['field'], school=data['school'], start_month=data['start_month_edu'],
        start_year=data['start_year_edu'], end_month=data['end_month_edu'], end_year=data['end_year_edu'],
        description=description, user_id=current_user.id)
    db.session.add(edu)
    db.session.commit()
    return jsonify({"success": True, "settingType": 'e', "edu_id": edu.id, "edu": edu.field})

@setting.route('/setting/security', methods=['POST'])
@login_required
def setting_security():
    data = request.get_json(force=True)
    password = data['password']
    new_password = data['new_password']
    confirm_password = data['confirm_password']
    if len(new_password) < 6 or new_password != confirm_password or not check_password_hash(current_user.password, password):
        return jsonify({"success": False, "msg": "Hata oluştu"})
    else:
        current_user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        return jsonify({"success": True, "msg": "Guvenlik ayarlarınız değişti."})

@setting.route('/deleteItem', methods=['POST'])
@login_required
def deleteItem():
    data = request.get_json(force=True)
    itemType, itemId = data['type_id'].split('_')
    if itemType == 'w':
        #item = WorkExperiences.query.filter_by(id=itemId).first()
        #db.session.delete(item)
        return jsonify({"success": True})
    elif itemType == 's':
        item = Skills.query.filter_by(id=itemId).first()
        current_user.UserSkills.remove(item)
        current_user.check_status()
        db.session.commit()
        return jsonify({"success": True})

@setting.route('/setting')
@login_required
def setting_page():
    with open("category.json", encoding='utf-8') as category:
        categories = json.load(category)
    with open("cities.json", encoding='utf-8') as city:
        cities = json.load(city)
    if current_user.status == 'company':
        return render_template('setting/companySetting.html', last_updated=last_updated, categories=categories, cities=cities)
    else:
        skills = current_user.UserSkills.all()
        workExps = WorkExperiences.query.filter_by(Worker=current_user).all()
        edus = Educations.query.filter_by(student=current_user).all()
        return render_template('setting/settings.html', last_updated=last_updated, skills=skills,
            workExps=workExps, edus=edus, categories=categories, cities=cities)
