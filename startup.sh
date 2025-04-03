#!/bin/bash

echo "Installing dependencies via TOML file... (pip install .)"
pip install .

echo "Installing editable mode... (pip install -e .)"
pip install -e .

echo "Running load_data script..."
load_data

echo "Running start script..."
start