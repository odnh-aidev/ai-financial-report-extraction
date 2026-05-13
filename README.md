# AI Financial Report Extraction

An end-to-end pipeline for extracting structured financial data 
from earnings reports using RAG and LLM-based structured output.

## Stack
- Python, Gemini API (generation + embeddings)
- FAISS (local vector search) → Databricks Vector Search
- MLflow experiment tracking
- Delta Lake + Unity Catalog

## Project Structure
- `src/generator.py` — synthetic earnings report generation
- `src/chunker.py` — document chunking with sliding window
- `src/retriever.py` — RAG retrieval pipeline

## Status
🚧 In progress — Week 1 of 6