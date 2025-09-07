# Smart Newsletter Project

## Overview

A Streamlit application for ingesting, clustering, summarizing, and exploring news articles from RSS feeds or Zotero databases. The app uses AI-powered summarization, multi-turn QA, and trend tracking to help users quickly grasp new information in their field.

## Goals
- Ingest and preprocess weekly news articles
- Cluster articles using embeddings and dynamic clustering
- Generate AI-powered summaries and allow manual editing
- Provide multi-turn question answering across articles
- Visualize clusters and trends over time
- Support filtering, exporting, and user management
- Ensure robust error handling and thorough testing

# how to dependency
```
conda activate smart_rss 
conda install python=3.11
pip install uv
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt
```

# Pre-commit hooks
```
# install pre-commit hooks
pre-commit install
# run black
pre-commit run black --all-files
```

# Running Tests
To run all unittests:
```
python -m unittest discover tests
```
Or to run a specific test file:
```
python -m unittest tests/test_grouping.py
```

# Checking Test Coverage
To check test coverage, first install coverage if not already installed:
```
uv pip install coverage
```
Then run:
```
coverage run -m unittest discover tests
coverage report -m
```
For an HTML report:
```
coverage html
# Open htmlcov/index.html in your browser
```

# Integration test with streamlit
```
pytest tests/test_app_integration.py
```

# Starting a uv project
[reference](https://docs.astral.sh/uv/guides/projects/)
```
uv init
uv add -r requirements.txt
uv pip install -e .
uv run ...
```
