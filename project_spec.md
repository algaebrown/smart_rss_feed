Absolutely! Here’s a **comprehensive, developer-ready specification** for your Streamlit news summarization app, based on all the details we’ve iteratively defined:

---

# Streamlit News Summarization & QA App – Developer Specification

## 1. **Project Overview**

Build a Streamlit application that ingests a week’s worth of RSS feed articles (via Zotero DB or master\_feed.xml), clusters them using embeddings, generates AI-powered summaries, allows multi-turn QA, and provides trend tracking over time. Users can filter, explore, and export content. The app is designed for users who need to quickly grasp new information in their field, with both high-level breadth and optional depth exploration.

---

## 2. **Primary Features**

### 2.1 User Experience & Layout

* **Target Users**: Researchers or professionals who need to read large volumes of news/articles.
* **Tabs**:

  1. **Overview** – High-level view of the week’s content (t-SNE/UMAP plot).
  2. **Cluster View** – Drill-down into individual clusters with AI-generated summaries.
  3. **QA Interface** – Multi-turn question answering across articles.
* **Multi-Turn QA**: Context is maintained across questions in a session.
* **Filtering**: Users can filter by keywords and/or source.
* **Exporting**:

  * Summaries (newsletter-style blurbs) → Markdown/CSV.
  * Cluster details → Markdown/CSV.
* **Editing**: Users can manually edit AI-generated summaries before export.

### 2.2 Visualization

* **t-SNE/UMAP Plot**:

  * Interactive scatterplot of article embeddings.
  * Hover shows article metadata.
  * Static per week (computed once).
* **Trend Charts**:

  * Line charts tracking cluster/article counts over the past year.
* **Cluster-Level Summaries**:

  * Bullet-point digest + narrative blurb side-by-side.

### 2.3 User Management & Persistence

* **Authentication**: Google OAuth2 login.
* **Persistence**: Store user state (expanded clusters, filters, QA history, edited summaries) across sessions.
* **Data Retention**: Maintain weekly data for up to **1 year**.

---

## 3. **Data Handling**

### 3.1 Inputs

* **Sources**:

  1. Zotero SQLite database.
  2. master\_feed.xml.
* **Level**: Article-level only (title, abstract/description, metadata).
* **Preprocessing**:

  * Extract key metadata: title, abstract, publication date, source, URL.
  * Remove duplicates.
  * Normalize text for embedding.

### 3.2 Embeddings

* Use **Hugging Face open-source embedding model** (sentence-level embeddings).
* Store embeddings for clustering and QA.

### 3.3 Clustering

* Use **dynamic clustering** (HDBSCAN or equivalent) to adapt to weekly content.
* Store cluster assignments alongside article metadata.

### 3.4 Summarization

* **AI-generated**:

  * Bullet-point digest.
  * Narrative newsletter-style blurb.
* **Manual editing** supported.
* **Trend detection**: Compare current week’s clusters/topics to previous weeks to highlight rising/decreasing/new topics.

### 3.5 QA

* **RAG-style QA**:

  * Primarily grounded in ingested articles.
  * Supplemented with external knowledge for context.
* **Multi-turn conversation**: Context maintained across questions.

### 3.6 Exports

* Summaries → Markdown / CSV.
* Clusters → Markdown / CSV.

---

## 4. **Architecture & Technology Stack**

| Layer              | Technology / Tool                                  |
| ------------------ | -------------------------------------------------- |
| Frontend           | Streamlit                                          |
| Visualization      | Plotly or Altair for interactive plots             |
| Embeddings         | Hugging Face transformer embeddings                |
| Clustering         | HDBSCAN / t-SNE / UMAP                             |
| Summarization & QA | OpenAI API or other LLM integration                |
| Storage            | Local SQLite or Postgres (user state, weekly data) |
| Authentication     | Google OAuth2                                      |
| Data Input         | Zotero SQLite / XML parser                         |

**Data Flow:**

1. Ingest articles (Zotero DB or XML).
2. Preprocess text and metadata.
3. Compute embeddings.
4. Perform dynamic clustering.
5. Generate AI summaries (cluster-level).
6. Visualize clusters (t-SNE/UMAP).
7. Allow filtering, QA, editing, and exporting.
8. Store user state and weekly data in database.

---

## 5. **Error Handling & Edge Cases**

* **Data ingestion errors**:

  * Invalid DB/XML → show error with actionable message.
  * Missing fields → skip article with warning logged.
* **Embedding failures**: Retry failed embeddings; log issues.
* **Clustering failures**: Default to a single cluster if HDBSCAN fails.
* **QA failures**: Graceful fallback → return “No relevant information found” with logging.
* **Authentication errors**: Redirect to login page; log failed attempts.
* **Export errors**: Validate write permissions; fallback to download in browser memory.

---

## 6. **Testing Plan**

### 6.1 Unit Tests

* Metadata extraction (Zotero DB/XML parsing).
* Embedding computation.
* Clustering logic and cluster assignment.
* Summarization generation (check output format).
* QA retrieval correctness.
* Export functions (Markdown/CSV).

### 6.2 Integration Tests

* End-to-end pipeline for one week of articles.
* t-SNE/UMAP plot rendering.
* Filter and search interactions.
* Multi-turn QA session persistence.
* Trend line charts update correctly with historical data.

### 6.3 User Acceptance Testing

* Verify UI usability across tabs.
* Validate manual summary editing and export.
* Confirm Google authentication flow and persistence.

### 6.4 Performance Testing

* Test with 500–1000 articles/week for embedding, clustering, and summarization latency.
* Test QA responsiveness with multi-turn sessions.

---

## 7. **Future Extensions**

* Support multiple domains/fields with separate feed sets.
* Allow users to add/manage custom RSS feeds.
* Incorporate full-text article embeddings.
* Notifications/alerts for trending topics.
* Advanced visualization (heatmaps, interactive line charts by cluster).


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

