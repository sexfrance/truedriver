# Manual PyPI Publishing Guide

## Prerequisites
```bash
pip install build twine
```

## Build the package
```bash
python -m build
```

## Upload to PyPI
```bash
# Test PyPI first (optional)
twine upload --repository testpypi dist/*

# Real PyPI
twine upload dist/*
```

## Notes
- You'll need a PyPI account and API token
- Store token in ~/.pypirc or use `twine upload --username __token__ --password YOUR_TOKEN`
