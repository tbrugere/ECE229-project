'''
This file tests the functions in predction.py
To generate a html coverage report, run
pytest --cov-report html:cov_html
        --cov=carsreco
'''
import pytest
import numpy as np
import pandas as pd
from carsreco import prediction


@pytest.fixture()
def setup():
    """Tests the functionality of estimate_parameters.
    """
    mock_df =  pd.DataFrame(columns=['model','manufacturer','price','posting_date'],
                            data =[['camry', 'abc',10000, '2021-05-04 17:30:00'],
                                   ['silverado', 'def',7000, '2021-04-04 09:30:00'],
                                   ['fx-150', 'ford', 12000, '2021-06-04 17:30:00'],
                                   ['camry', 'abc', 20000, '2021-06-04 16:30:00'],
                                   ['camry', 'abc', 25000, '2021-05-04 09:30:00'],
                                   ['fx-150', 'ford', 15000, '2021-05-04 16:00:00']])
    mock_df['posting_date'] = pd.to_datetime(mock_df['posting_date'])
    return mock_df

def test_estimate_parameters_general(setup):
    """Tests the functionality of estimate_parameters.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    predict = prediction.IntervalPricePrediction(mock_df)
    params = predict.estimate_parameters()
    assert params['posting_date']['max'].dtype == 'datetime64[ns]'
    assert params['posting_date']['min'].dtype == 'datetime64[ns]'
    assert sum(params['price']['std'] < 0) == 0
    assert sum(params['model']['count'] < 0) == 0

def test_estimate_parameters_mock_data(setup):
    """Tests the estimate_parameters function on mock data.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    predict = prediction.IntervalPricePrediction(mock_df)
    params = predict.estimate_parameters()
    assert params.loc['camry']['price']['mean'] == np.mean([10000, 20000, 25000])
    assert round(params.loc['camry']['price']['std']) == round(np.std([10000, 20000, 25000], ddof=1))
    assert str(params.loc['camry']['posting_date']['max']) == '2021-06-04 16:30:00'

def test_get_CI(setup):
    """Tests the get_CI function on mock data.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    predict = prediction.IntervalPricePrediction(mock_df)
    predict.model_params = predict.estimate_parameters()
    results = predict.get_CI(18000, 19000)
    assert len(results[0]) == 5
