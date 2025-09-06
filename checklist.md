# Smart Newsletter Project Checklist

## 1. Project Setup
- [x] Initialize git repository
- [x] Create README.md with project overview
- [x] Set up folder structure: src/, tests/, docs/

## 2. Data Models
- [x] Define newsletter model (title, content, publication date)
- [x] Write unit tests for newsletter model
- [x] Implement newsletter CRUD operations
- [x] Define user model (email, password hash, profile info)
- [x] Write unit tests for user model
- [x] Implement user CRUD operations
- [x] Define subscription model (user-newsletter link)
- [x] Write unit tests for subscription model
- [x] Implement subscription CRUD operations

## 3. Content Pipeline
- [x] Implement content ingestion logic
- [x] Write tests for content ingestion
- [x] Implement content formatting logic
- [x] Write tests for content formatting

## 4. User Management
- [ ] Implement user registration
- [ ] Write tests for registration
- [ ] Implement authentication
- [ ] Write tests for authentication
- [ ] Implement profile management
- [ ] Write tests for profile management

## 5. Subscription Logic
- [ ] Implement subscribe functionality
- [ ] Write tests for subscribe
- [ ] Implement unsubscribe functionality
- [ ] Write tests for unsubscribe

## 6. Email Delivery
- [ ] Integrate email sending functionality
- [ ] Write tests for email delivery
- [ ] Implement scheduling logic
- [ ] Write tests for scheduling

## 7. Admin Dashboard
- [x] Build newsletter management interface (Streamlit dashboard for viewing newsletters)
- [ ] Write tests for newsletter management
- [ ] Build user management interface
- [ ] Write tests for user management

## 8. Testing
- [ ] Write integration tests for all features
- [ ] Run and review test coverage

## 9. Deployment
- [ ] Prepare deployment scripts
- [ ] Finalize documentation

## 10. Embeddings & Clustering
- [ ] Implement logic to compute sentence/article embeddings (Hugging Face model)
- [ ] Write tests for embedding computation
- [ ] Implement dynamic clustering (HDBSCAN/t-SNE/UMAP)
- [ ] Write tests for clustering and cluster assignment

## 11. AI Summarization & QA
- [ ] Integrate LLM/AI summarization for cluster-level bullet/narrative blurbs
- [ ] Write tests for summarization output format
- [ ] Implement multi-turn QA interface (RAG-style, context maintained)
- [ ] Write tests for QA retrieval and context

## 12. Visualization & Trends
- [ ] Visualize clusters and summaries in Streamlit dashboard (scatterplot, cluster view)
- [ ] Implement trend detection and visualization (line charts, topic changes)
- [ ] Write tests for visualization and trend logic