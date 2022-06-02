"""
Deploying scripts
=====================================

Those scripts are used for the deploying

You should not have to call them directly, and should rather use the make command to call them

Data preprocessing
-------------------

.. argparse::
    :module: scripts.preprocessing
    :func: get_argparser
    :prog: scripts/preprocessing.py


Deploying script
-------------------

This script will deploy

Usage: ::

    scripts/deploy.sh

It does not take any argument, but will read the `$SERVER`, `$REPO` and `$DEPLOYBRANCH` variables if they are defined
"""
