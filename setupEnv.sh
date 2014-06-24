#!/usr/bin/env bash

export CONSOLE_DIR=`pwd`
export PYTHONPATH=$PYTHONPATH:$CONSOLE_DIR
python createConfig/createConfig.py
