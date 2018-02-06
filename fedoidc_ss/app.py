from flask.app import Flask
from fedoidc_ss import database
from urllib.parse import quote_plus


def init_fedoidc_ss(app):
    database.init_db()

def init_app(name=None):
    name = name or __name__
    app = Flask(name)
    app.config.from_pyfile('config.py')
    app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)

    init_fedoidc_ss(app)

    from fedoidc_ss.views import sigserv

    app.register_blueprint(sigserv)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        database.db_session.remove()

    return app

