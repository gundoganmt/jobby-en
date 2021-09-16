from jobby import create_app, socketio
from jobby.models import Users, Tasks

import flask_whooshalchemy as wa

app = create_app()
wa.whoosh_index(app, Tasks)
wa.whoosh_index(app, Users)

if __name__ == '__main__':
    socketio.run(app, debug=True)
