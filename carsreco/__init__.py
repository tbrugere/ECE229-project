"""Cars recommendation dashboard in python

This package contains all the code that supports running the dashboard.



"""

from .dashboard import create_app
import flask

def create_server() -> flask.Flask:
    """Creates the server object

    Creates the dashboard using 

    Returns:
        flask.Flask: Flask object used by the wsgi to run the dashboard
    """
    app = create_app()
    assert isinstance(app.server, flask.Flask)
    return app.server
