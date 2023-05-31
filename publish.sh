rm -rf dist
rm -rf pyattr.egg-info

python -m build

twine upload dist/*