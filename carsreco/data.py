import pandas as pd

df = pd.read_csv('data/preprocessed.csv', index_col=0, parse_dates=["posting_date"])
