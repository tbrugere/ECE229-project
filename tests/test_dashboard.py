''' This file tests the functions in dashboard.py
To generate a html coverage report, run
pytest --cov-report html:cov_html
        --cov=carsreco'''
import pytest
from carsreco import dashboard
import dash

def test_create_app():
    assert isinstance(dashboard.create_app(), dash.Dash)
