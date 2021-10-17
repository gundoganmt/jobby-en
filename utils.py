import os
from flask_mail import Message
from flask_login import current_user
from threading import Thread
from flask import current_app, render_template, abort, url_for, redirect
from flask_mail import Mail
from functools import wraps
mail = Mail()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(name, email, subject, message):
    app = current_app._get_current_object()
    msg = Message(subject='Jobby Contact',
        sender="support@jobby.net",
        recipients=["mahmut_gundogan@hotmail.com"])
    msg.body = "name: {}, email: {}, subject: {}, message: {}".format(name, email, subject, message)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def send_confirmation_email(user):
    app = current_app._get_current_object()
    token = user.get_confirmation_token()
    msg = Message(subject='Confirmation email',
        sender="support@jobby.net",
        recipients=[user.email])
    msg.html = render_template('account/email_confirmation.html', token=token, name=user.name)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
        for root_path, dirs, files in os.walk(folder)
        for f in files))

ALLOWED_IMG_EXTENSIONS = {'jpeg', 'jpg', 'png'}
ALLOWED_OFFER_EXTENSIONS = {'docx', 'doc', 'pdf'}

UPLOAD_IMG_FOLDER = os.path.join(os.getcwd(), 'jobby/static/images')
UPLOAD_TASK_FOLDER = os.path.join(os.getcwd(), 'jobby/static/images/taskpics')
UPLOAD_OFFER_FOLDER = os.path.join(os.getcwd(), 'jobby/static/files')

def allowed_img_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def allowed_offer_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_OFFER_EXTENSIONS

def get_extension(filename):
    return '.'+ filename.rsplit('.', 1)[1].lower()

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_user.is_authenticated:
                try:
                    if current_user.is_admin:
                        return fn(*args, **kwargs)
                except:
                    abort(404), 404
            return redirect(url_for('account.adminlogin'))
        return decorator
    return wrapper

def get_category(categor_num):
    categories = {
        '1': 'Programming',
        '2': 'Writing',
        '3': 'Graphics Design',
        '4': 'Digital Marketing',
        '5': 'Data Science',
        '6': 'Video & Animation',
        '7': 'Lifestyle',
        '8': 'Finance',
        '9': 'Other'
    }

    return categories.get(categor_num)
