#!/bin/env python3
"""
Preprocessing script.
This script should be run once at each deployment on the server
"""
from argparse import ArgumentParser
from pathlib import Path
import logging
from logging import info


import numpy as np
import pandas as pd

def preprocess(input_file, output_file, drops=['condition', 'size']) -> None:
    '''
    Preprocesses the dataset by converting posting date to datetime
    and adding ranges to price/year.

    Args:
        input_file: the original (input) dataset csv
        output_file: the processed dataset csv
        drops: list of columns to drop
    '''
    df: pd.DataFrame = pd.read_csv(input_file, header=0, index_col=0)#type: ignore

    all_drops = ['url', 'region_url'] + drops
    df.drop(all_drops, inplace=True, axis=1)
    info(f"there are { len(df['manufacturer'].unique()) } unique manufacturers")

    # Correction of previous columns
    df['state'] = df['state'].str.upper()
    info('correcting state')
    # df['posting_date'] = pd.to_datetime(df['posting_date'], format='%Y-%m-%dT%H:%M:%S', cache=True)
    info('processing date')
    df['posting_date'] = pd.to_datetime(df['posting_date'], utc=True, infer_datetime_format=True, cache=True)
    df['posting_year'] = pd.DatetimeIndex(df['posting_date']).year
    df['posting_month'] = pd.DatetimeIndex(df['posting_date']).month

    info('processing price')
    df['price'] = df['price'].replace(0, np.nan)
    df = df.dropna(subset=['price'])#type: ignore
    df = df[df['price'] < 300000]

    info('adding ranges')
    df['price_range'] = pd.cut(df['price'],
                               [-np.inf, 5000, 15000, 25000, np.inf],
                               labels=['<$5000', '$5000-15000', '$15000-25000', '>$25000']
                               )
    df['year_range'] = pd.cut(df['year'],
                               [-np.inf, 2005, 2010, 2015, np.inf],
                               labels=['<2005', '2005-2010', '2010-2015', '>2015']
                               )
    df['odometer_range'] = pd.cut(df['odometer'],
                              [-np.inf, 40000, 80000, 120000, np.inf],
                              labels=['<40000', '40000-80000', '80000-120000', '>120000']
                              )
    df.to_csv(output_file)



def get_argparser() -> ArgumentParser:
    """Returns the argument parser of the module
    """
    parser = ArgumentParser(description=__doc__)

    parser.add_argument("input", type=Path,  help="Original (inputed) csv")
    parser.add_argument("output", type=Path,
                        help="Preprocessed csv output file")

    parser.add_argument("--drop", default=['condition', 'size'], nargs="*", type=str, 
                        help=("columns to drop (default [condition, size], "
                              "use --drop with no argument to drop nothing)" ))

    parser.add_argument( '-log',
                     '--loglevel',
                     default='info',
                     help='Provide logging level. Example --loglevel debug, default=info' )

    return parser

if __name__ == "__main__":
    parser = get_argparser()
    arguments = parser.parse_args()
    logging.basicConfig( level=arguments.loglevel.upper() )
    preprocess(arguments.input, arguments.output, arguments.drop)
