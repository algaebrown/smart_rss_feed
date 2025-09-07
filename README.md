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
