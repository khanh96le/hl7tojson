rm -rf dist
python setup.py sdist bdist_wheel

# Update to testing domain
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Update to real domain
twine upload dist/*
