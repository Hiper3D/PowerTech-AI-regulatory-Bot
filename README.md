# 🤖 Enterprise AI Regulatory Agent

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge)

## 📌 Executive Overview
This package houses the backend source code for an enterprise-grade AI (Artificial Intelligence - the simulation of human intelligence by machines) regulatory agent engineered for Power Tech Consultant. 

Utilizing a robust RAG (Retrieval-Augmented Generation - an AI framework that retrieves facts from an external knowledge base to ground large language models) architecture, this self-contained Python application leverages OpenAI's GPT-4o (Generative Pre-trained Transformer - a type of large language model designed to generate human-like text) and FAISS (Facebook AI Similarity Search - a library for efficient similarity search and clustering of dense vectors) to autonomously ingest, vectorize, and answer highly domain-specific regulatory and tariff inquiries.

## 🏗️ Core Architecture & Capabilities



* **Vector Search Engine:** Implemented FAISS (Facebook AI Similarity Search - a library for efficient similarity search and clustering of dense vectors) to efficiently index and retrieve contextual embeddings from complex regulatory documents.
* **Persistent Data Ingestion:** Provisioned an administrative endpoint to seamlessly ingest PDF (Portable Document Format - a file format used to present and exchange documents reliably) files. Extracted text is vectorized and persistently stored, eliminating the need for redundant training cycles upon server reboot.
* **Decoupled Integration:** Engineered to support both a lightweight frontend HTML (HyperText Markup Language - the standard code used to structure a web page) widget and secure server-to-server endpoints for enterprise systems like a CRM (Customer Relationship Management - a technology for managing all your company's relationships and interactions with customers) or ERP (Enterprise Resource Planning - a type of software that organizations use to manage day-to-day business activities).

## ⚙️ Environment Provisioning & Initialization

### 1. Dependency Installation
Extract the repository architecture and initialize the environment via your local CLI (Command Line Interface - a text-based interface for running commands):
```bash
pip install -r requirements.txt
