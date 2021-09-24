from flask import render_template, Blueprint, request, url_for, jsonify
from flask_login import current_user, login_required
from jobby.models import Bids, Tasks, Users, Views, Notification, Reviews, Offers, Messages
from jobby import db

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
            return render_template('admin/tables.html', users=users)
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
    users = Users.query.all()
    return render_template('admin/views.html', users=users)

@admin.route('/delete-user/<user_id>')
def deleteUser(user_id):
    return jsonify({'success': True})
