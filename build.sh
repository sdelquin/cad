#!/bin/bash

cd "$(dirname "$0")"
source ~/.virtualenvs/cad/bin/activate
exec python cad.py
