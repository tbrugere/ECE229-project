''' This file tests the functions in dashboard.py
To generate a html coverage report, run
pytest --cov-report html:cov_html
        --cov=carsreco'''
import imp
from numpy import isin
import pytest
from carsreco import dashboard, prediction
import dash
import types
import numpy as np
import pandas as pd
import dash_html_components as html

codeAttribute = '__code__'

def test_create_app():
    assert isinstance(dashboard.create_app(), dash.Dash)

# hack to test the inner functions of the factory method
def freeVar(val):
  def nested():
    return val
  return nested.__closure__[0]

def nested(outer, innerName, **freeVars):
  if isinstance(outer, (types.FunctionType, types.MethodType)):
    outer = outer.__getattribute__(codeAttribute)
  for const in outer.co_consts:
    if isinstance(const, types.CodeType) and const.co_name == innerName:
        return types.FunctionType(const, globals(), None, None, tuple(
            freeVar(freeVars[name]) for name in const.co_freevars))

def test_update_output():
    nested_update = nested(dashboard.create_app, 'update_output', dropdown_select=lambda k: html.Div())
    assert isinstance(nested_update("state"), html.Div)