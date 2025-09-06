
# Smart Newsletter Dashboard: Updated Project Spec

## Overview
A modular Streamlit dashboard for ingesting, embedding, filtering, visualizing, and exporting newsletter articles. All state is session-persistent and all actions update the `filters` attribute of each newsletter.

## Workflow
1. **Startup**
    - Load newsletters from the feed automatically on app start
    - Store newsletters in session state
2. **Embedding & t-SNE**
    - Compute embeddings for all loaded newsletters
    - Compute t-SNE coordinates for all newsletters
    - Store embeddings and t-SNE in each newsletter object
3. **Filtering**
    - **Date filter**: User sets date range; update `filters['date_filter']` for each newsletter
    - **AI filter**: User provides prompt and filter name; result stored in `filters[ai_filter_key]`
    - **Keyword filter**: User provides keyword; update `filters['f{keyword}']` for exact title match
4. **Article Display**
    - User can select one or more filters to show articles (AND/OR logic as needed)
    - Display filtered articles with all details
5. **Visualization**
    - User can select a filter to visualize on t-SNE plot (color by filter)
    - User can select a filter to visualize on dendrogram
6. **Export**
    - User can select articles from the filtered list
    - Export selected articles as CSV (all fields in Newsletter class)

## Data Model
- **Newsletter class**: title, content, publication_date, url, embedding, tsne, filters (dict)

## UI/UX
- Sidebar: date filter, AI filter, keyword filter, filter selection, export button
- Main: t-SNE plot, dendrogram, filtered articles list (with selection checkboxes)
- All filter actions update the `filters` dict in each newsletter
- All visualizations and exports reflect current filter selection

## Requirements
- No redundant ingestion/embedding
- Modular, testable functions for each step
- Clear feedback to user for each action
- All state is session-persistent


## 8. **LLM Layer**

### 8.1 Purpose

* Orchestrate **summarization**, **QA**, and **trend analysis**.
* Support multi-turn QA with memory/context.

### 8.2 Frameworks

* **LlamaIndex** or **LangChain** to manage:

  * Document ingestion.
  * Indexing embeddings.
  * Query routing.
  * Multi-turn memory.

### 8.3 Models

* **Vertex AI Gemma** (cloud, free tier)
* **Ollama local Gemma3b** (local, privacy-friendly)

### 8.4 Workflow

1. LlamaIndex/LangChain ingests **article metadata and embeddings**.
2. Indexes documents for RAG-style retrieval.
3. Summarization and trend detection queries routed through **Gemma**.
4. QA requests use:

   * RAG from weekly articles.
   * Supplement with external knowledge from LLM.
5. Multi-turn context stored in session/persistent memory.

### 8.5 Configuration Options

* User or developer can **switch backend**:

  * `vertex_ai` → call Gemma via API.
  * `ollama_local` → call Gemma3b locally.

### 8.6 Error Handling

* Failover:

  * If cloud API unavailable → fallback to local Ollama model (if configured).
  * Timeout/connection errors → return informative message to user.

---

## 9. **Updated Architecture & Technology Stack**

| Layer             | Technology / Tool                               |
| ----------------- | ----------------------------------------------- |
| Frontend          | Streamlit                                       |
| Visualization     | Plotly or Altair                                |
| Embeddings        | Hugging Face embeddings                         |
| Clustering        | HDBSCAN / t-SNE / UMAP                          |
| LLM Orchestration | **LlamaIndex** or **LangChain**                 |
| LLM Models        | Vertex AI Gemma (cloud), Ollama Gemma3b (local) |
| Storage           | SQLite / Postgres (user state, weekly data)     |
| Authentication    | Google OAuth2                                   |
| Data Input        | Zotero SQLite / master\_feed.xml                |

---

## 10. **Notes for Developer**

* **Indexing & Retrieval**: Use LlamaIndex/LangChain to create a **vector index** of articles with embeddings.
* **Summarization**:

  * Cluster-level: bullet + narrative.
  * Trend detection: compare current cluster vectors to historical vectors.
* **QA**: LLM queries the index first, then supplements with model knowledge.
* **Multi-turn memory**: Implement session or DB persistence via LlamaIndex/LLM memory module.

