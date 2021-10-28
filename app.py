from jobby import create_app, socketio, db
from jobby.models import Users, Tasks, Admin, SiteSettings
from werkzeug.security import generate_password_hash
import flask_whooshalchemy as wa

app = create_app()
wa.whoosh_index(app, Tasks)
wa.whoosh_index(app, Users)

@app.before_first_request
def populateDb():
    admin = db.session.query(Admin).first()
    ss = db.session.query(SiteSettings).first()
    if not admin:
        admin = Admin(username='admin', email="admin@gmail.com", full_name="John Doe",
            password=generate_password_hash("123456", method='sha256'))
        db.session.add(admin)
        db.session.commit()
    if ss:
        app.config.update(
            MAIL_SERVER=ss.mail_server,
            MAIL_PORT=ss.port,
            MAIL_USE_TLS = ss.use_TLS,
            MAIL_USE_SSL = ss.use_SSL,
            MAIL_USERNAME = ss.username,
            MAIL_PASSWORD = ss.password,
            MAIL_DEFAULT_SENDER = ss.default_sender
        )
    return True

if __name__ == '__main__':
    socketio.run(app, debug=True)
