rmdir dist /s /q
rmdir pyattr.egg-info /s /q

python -m build

twine upload dist/*