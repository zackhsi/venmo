#!/bin/bash
set -e

rm -rf dist/*

echo "Building Source and Wheel (universal) distribution..."
python setup.py sdist bdist_wheel --universal

echo "Uploading the package to PyPi via Twine..."
twine upload dist/*
