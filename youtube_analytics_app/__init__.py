"""Initialize Flask app."""
from flask import Flask



def init_app():
    """Construct core Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    # Note: A secret key is included in the sample so that it works.
    # If you use this code in your application, replace this with a truly secret
    # key. See https://flask.palletsprojects.com/quickstart/#sessions.
    # secrets.token_hex()
    app.secret_key = '7445bc149f2b79f5c0a71371ecf9c7fbd2853de80b32777b9da170596a2661f8'

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash Applications:
        from .dashboards.sample_dash import init_dashboard
        app = init_dashboard(app)

        return app