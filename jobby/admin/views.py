from flask import render_template, Blueprint, request, url_for, jsonify, redirect
from flask_login import current_user, login_required
from jobby.models import (Bids, Tasks, Users, Views, Notification,
    Reviews, Offers, Messages, Categories, Skills, WorkExperiences, Educations)
from jobby import db
from PIL import Image
from datetime import datetime
from utils import crop_max_square, allowed_img_file, get_extension, UPLOAD_IMG_FOLDER
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os, uuid

admin = Blueprint('admin',__name__)

@admin.route('/adminpanel', methods=['GET', 'POST'])
def adminpanel():
    return render_template('admin/index.html')

@admin.route('/adminpanel/<table>/<int:item_id>')
@admin.route('/adminpanel/<table>', defaults={'item_id': None}, methods=['GET', 'POST'])
def dbop(table, item_id):
    if table == 'users':
        if item_id:
            user = Users.query.get(item_id)
            return render_template('admin/users.html', user=user)
        else:
            users = Users.query.all()
            return render_template('admin/usersTable.html', users=users)
    elif table == 'projects':
        if item_id:
            project = Tasks.query.get(item_id)
            return render_template('admin/projects.html', project=project)
        else:
            projects = Tasks.query.all()
            return render_template('admin/projectsTable.html', projects=projects)
    elif table == 'email-settings':
        return render_template('admin/email-settings.html')
    elif table == 'create-admin':
        return render_template('admin/create-admin.html')
    elif table == 'bids':
        bids = Bids.query.all()
        return render_template('admin/bidsTable.html', bids=bids)
    elif table == "messages":
        msgs = Messages.query.all()
        return render_template('admin/messagesTable.html', msgs=msgs)

@admin.route('/adminpanel/create/<table>', methods=['GET', 'POST'])
def create(table):
    if request.method == 'GET':
        if table == 'messages':
            users = Users.query.all()
            return render_template('admin/createMessage.html', users=users)
        elif table == 'users':
            return render_template('admin/createUser.html')
        elif table == 'categories':
            return render_template('admin/createCategories.html')
        elif table == 'projects':
            return render_template('admin/createProjects.html')
    else:
        if table == 'messages':
            return "success"
        elif table == 'categories':
            category = request.form['category']
            print(category)
            if not category:
                return jsonify({'success': False, 'msg': "Cannot create empty category!"})
            cat = Categories(category=category)
            db.session.add(cat)
            db.session.commit()
            print("here")
            return jsonify({'success': True})

@admin.route('/adminpanel/chart/<view_type>')
def views(view_type):
    if view_type == 'users':
        users = Users.query.filter_by(status='freelancer').all()
        return render_template('admin/views.html', users=users)

@admin.route('/user-view-data/<username>')
def userViewData(username):
    user = Users.query.filter_by(username=username).first()
    views = Views.query.filter_by(user_id=user.id).first()
    return jsonify({views.monday, views.tuesday, views.wednesday, views.thursday,
        views.friday, views.saturday, views.sunday})

@admin.route('/createUser', methods=['POST'])
def createUser():
    name = request.form['name']
    surname = request.form['surname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phone_number = request.form['phone']

    if len(username) < 6 or not username.isalnum():
        return jsonify({'success': False, 'msg': "You have to provide valid username."})

    if Users.query.filter_by(username=username).first():
        return jsonify({'success': False, 'msg': "This username allready being used!"})

    if len(password) < 6:
        return jsonify({'success': False, 'msg': "You have to provide valid password. At least 6 character"})

    if len(name) < 3 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        return jsonify({'success': False, 'msg': "The length of name and surname should be between 3 and 30"})

    if len(email) > 50:
        return jsonify({'success': False, 'msg': "Incorrect Email!"})

    if Users.query.filter_by(email=email).first():
        return jsonify({'success': False, 'msg': "This email allready being used!"})

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

@admin.route('/adminpanel/editUser/<int:user_id>')
def editUser(user_id):
    if request.method == 'GET':
        user = Users.query.get(user_id)
        return render_template('admin/editUser.html', user=user)

@admin.route('/editUser/personel/<int:user_id>', methods=['POST'])
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

    if len(email) > 50:
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
def profile(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'success': False, "msg": 'Error occured. Refresh the page please!'})
    user.field_of_work = request.form['field_of_work']
    user.tagline = request.form['tagline']
    user.country = request.form['country']
    user.introduction = request.form['introduction']
    db.session.commit()
    return jsonify({'success': True, "editProfileType": 'pro'})

@admin.route('/editUser/skill/<int:user_id>', methods=['POST'])
def skill(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'success': False, "msg": 'Error occured. Refresh the page please!'})
    skill = request.form['skill']
    level = request.form['level']
    sk = Skills(skill=skill, level=level, user_id=user.id)
    db.session.add(sk)
    db.session.commit()
    return jsonify({'success': True, "editProfileType": 's', "skill": skill, "level": level, "skill_id": sk.id})

@admin.route('/editUser/social/<user_id>', methods=['POST'])
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

    return jsonify({"success": True, "field": field, "school": school,
        "edu_id": edu.id, 'editProfileType': 'e', "duration": edu.start_month + " " + str(edu.start_year) + " - " + edu.end_month + " " + str(edu.end_year)})

@admin.route('/deleteItem/<type_id>')
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
        #current_user.check_status()
        db.session.commit()
        return jsonify({"success": True, 'currentField': 's'})
    elif itemType == 'e':
        item = Educations.query.get(itemId)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, 'currentField': 'e'})


@admin.route('/delete-user/<user_id>')
def deleteUser(user_id):
    return jsonify({'success': True})
