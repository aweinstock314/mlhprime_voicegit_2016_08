#!/bin/sh
pip install requests -t .
zip -r lambda.zip lambda_function.py ./requests*
