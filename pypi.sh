#!/usr/bin/env bash
python setup.py sdist bdist_wheel && twine upload ./dist/*
rm -rf ./build/ ./dist/ ./*.egg-info/
exit