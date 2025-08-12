#!/usr/bin/env bash

if [[ -x venv/bin/ipython ]]; then
    venv/bin/ipython -i sql_clients.py
elif [[ -x venv/bin/python ]]; then
    venv/bin/python -i sql_clients.py
else
    echo "Could not find venv/bin/ipython or venv/bin/python!" >&2
    exit 1
fi
