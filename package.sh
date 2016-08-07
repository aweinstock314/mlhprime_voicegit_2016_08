#!/bin/sh
pip install requests -t .
zip lambda.zip lambda_function.py ./requests*
