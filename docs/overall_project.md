# Docling API Service: Overall Project Design

## 1. Project Overview
- **Goal:** Provide robust, scalable API services for document parsing and information extraction using IBM DocLing.
- **Scope:** Expose endpoints for PDF and image ingestion, table and text extraction, and structured output (JSON, CSV, Markdown).

## 2. Key Features
- Upload documents (PDF, images)
- Extract tables, text, figures, and metadata
- Export results in multiple formats (JSON, CSV, Markdown)
- Support for batch processing
- Health and status endpoints

## 3. Architecture
- **API Layer:** FastAPI-based, modular, versioned endpoints
- **Service Layer:** Business logic, DocLing integration, error handling
- **Model Layer:** Pydantic schemas for requests/responses
- **External Services:** IBM DocLing, optional storage or queue integrations

## 4. Endpoints (Initial)
- `/docling/extract-tables-csv/` – Upload PDF, get tables as CSV (ZIP)
- `/docling/extract-json/` – Upload PDF, get full document as JSON
- `/docling/extract-markdown/` – Upload PDF, get Markdown
- `/health` – Health check

## 5. Data Flow
1. Client uploads document via API.
2. API validates and stores file temporarily.
3. Service layer invokes DocLing for extraction.
4. Results are formatted and returned to the client.

## 6. Non-Functional Requirements
- Scalability (support concurrent requests)
- Security (input validation, file size limits)
- Logging and monitoring
- Error handling and user-friendly messages

## 7. Future Extensions
- User authentication
- Async/batch processing
- Integration with cloud storage
- Support for more document types

---

# Project Phased Build Plan

This document outlines the phased approach for building the FastAPI project with IBM Docling integration, notebook support, and local tooling.

## Phase 1: Project Setup
- Create project directory structure
- Initialize FastAPI application
- Set up basic service structure
- Add initial dependencies (FastAPI, IBM Docling, etc.)

## Phase 2: IBM Docling Integration
- Implement core service(s) using IBM Docling
- Add endpoints for document parsing
- Test integration with sample data

## Phase 3: Notebook Support
- Set up Jupyter notebook environment
- Create example notebooks demonstrating service usage
- Document notebook workflows

## Phase 4: Local Tools & Utilities
- Add scripts/utilities for local testing
- Provide sample data and test cases in `data/`

## Phase 5: Documentation & Finalization
- Expand documentation
- Add usage examples and API references
- Prepare for deployment or further extension

## Required Frameworks and Libraries

- FastAPI – for building the REST API
- Uvicorn or uv – ASGI server to run FastAPI
- IBM Docling – for document parsing and information extraction
- PyPDF2 or pdfplumber – for PDF file handling (if pre-processing is needed before Docling)
- Pydantic – for request/response data validation (comes with FastAPI)
- python-multipart – for handling file uploads in FastAPI
- Jupyter – for notebook support (optional, for development and demos)

Example requirements (requirements.txt):

```
fastapi
uv
ibm-docling
pypdf2
python-multipart
jupyter
```

---

# Recommended Modular API Directory Structure

```
src/
├── api/                # FastAPI routers/endpoints
│   ├── __init__.py
│   ├── v1/             # Versioned API (optional, for future-proofing)
│   │   ├── __init__.py
│   │   ├── endpoints/  # Individual endpoint modules
│   │   │   ├── __init__.py
│   │   │   ├── docling.py
│   │   │   └── health.py
│   │   └── router.py   # Combines all endpoints
├── core/               # Core app config, startup, settings
│   ├── __init__.py
│   ├── config.py
│   └── logging.py
├── services/           # Business logic, Docling integration, etc.
│   ├── __init__.py
│   └── docling_service.py
├── models/             # Pydantic models (request/response schemas)
│   ├── __init__.py
│   └── docling_models.py
├── main.py             # FastAPI app entrypoint
```

This structure supports clean separation of API, business logic, and models, and is designed for scalability and maintainability.
