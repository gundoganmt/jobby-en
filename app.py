from jobby import create_app, socketio, db
from jobby.models import Users, Tasks, Admin, MailConfig
from werkzeug.security import generate_password_hash
import flask_whooshalchemy as wa

app = create_app()
wa.whoosh_index(app, Tasks)
wa.whoosh_index(app, Users)

@app.before_first_request
def populateDb():
    admin = db.session.query(Admin).first()
    config = db.session.query(MailConfig).first()
    if not admin:
        admin = Admin(username='admin', email="admin@gmail.com", full_name="John Doe",
            password=generate_password_hash("123456", method='sha256'))
        db.session.add(admin)
        db.session.commit()
    if config:
        app.config.update(
            MAIL_SERVER=config.mail_server,
            MAIL_PORT=config.port,
            MAIL_USE_TLS = config.use_TLS,
            MAIL_USE_SSL = config.use_SSL,
            MAIL_USERNAME = config.username,
            MAIL_PASSWORD = config.password
        )
    return True

if __name__ == '__main__':
    socketio.run(app, debug=True)
