from flask import render_template, Blueprint, request, url_for, jsonify
from flask_login import current_user, login_required
from jobby.models import Bids, Tasks, Users, Views, Notification, Reviews, Offers
from jobby import db

admin = Blueprint('admin',__name__)

@admin.route('/adminpanel', methods=['GET', 'POST'])
def adminpanel():
    return render_template('admin/index.html')

@admin.route('/admin/<table>/<int:item_id>')
@admin.route('/admin/<table>', defaults={'item_id': None}, methods=['GET', 'POST'])
def dbop(table, item_id):
    if table == 'users':
        if item_id:
            user = Users.query.get(item_id)
            return render_template('admin/users.html', user=user)
        else:
            users = Users.query.all()
            return render_template('admin/tables.html', users=users)
    if table == 'projects':
        if item_id:
            project = Tasks.query.get(item_id)
            return render_template('admin/projects.html', project=project)
        else:
            projects = Tasks.query.all()
            return render_template('admin/tables.html', projects=projects)


@admin.route('/delete-user/<user_id>')
def deleteUser(user_id):
    return jsonify({'success': True})
