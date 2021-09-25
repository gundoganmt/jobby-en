from flask import render_template, Blueprint, request, url_for, jsonify
from flask_login import current_user, login_required
from jobby.models import Bids, Tasks, Users, Views, Notification, Reviews, Offers, Messages
from jobby import db
from PIL import Image
from datetime import datetime
from utils import crop_max_square, allowed_img_file, get_extension, UPLOAD_IMG_FOLDER
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

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

@admin.route('/createUser/personal', methods=['POST'])
@login_required
def personal():
    name = request.form['name']
    surname = request.form['surname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phone_number = request.form['phone']

    if len(name) < 3 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        return jsonify({'success': False, 'msg': "The length of name and surname should be between 3 and 30"})

    if len(email) > 50:
        return jsonify({'success': False, 'msg': "Incorrect Email!"})

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = Users(username=username, name=name, surname=surname, email=email, phone_number=phone_number,
        password=hashed_password, member_since=datetime.utcnow(), status='employer', email_approved=True)

    db.session.add(new_user)
    db.session.commit()

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
    db.session.commit()
    return jsonify({'success': True, "editProfileType": 'p'})

@admin.route('/createUser/personal', methods=['POST'])
@login_required
def personal():
    field_of_work = request.form['field_of_work']
    tagline = request.form['tagline']
    country = request.form['country']



    return jsonify({'success': True, "editProfileType": 'p'})

@admin.route('/delete-user/<user_id>')
def deleteUser(user_id):
    return jsonify({'success': True})
