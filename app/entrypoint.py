from uwsgidecorators import postfork

import app


@postfork
def init_uwsgi():
    app.init(app.app)


worker = app.app
