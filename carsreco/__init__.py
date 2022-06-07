from .dashboard import create_app
import flask

def create_server() -> flask.Flask:
    app = create_app()
    assert isinstance(app.server, flask.Flask)
    return app.server
