#!/bin/bash
set -e

echo "Building Source and Wheel (universal) distribution..."
python setup.py sdist bdist_wheel --universal

echo "Uploading the package to PyPi via Twine..."
twine upload dist/*
