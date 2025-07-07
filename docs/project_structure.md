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

Update this document as the project progresses through each phase.

## Project Directory Structure (Table)

| Path                                      | Description                                      |
|--------------------------------------------|--------------------------------------------------|
| `src/`                                    | Project source root                              |
| ├── `api/`                                | FastAPI routers/endpoints                        |
| │   ├── `__init__.py`                     | API package init                                 |
| │   ├── `v1/`                             | Versioned API (optional, for future-proofing)    |
| │   │   ├── `__init__.py`                 | v1 package init                                  |
| │   │   ├── `endpoints/`                  | Individual endpoint modules                      |
| │   │   │   ├── `__init__.py`             | Endpoints package init                           |
| │   │   │   ├── `docling.py`              | Docling endpoints                                |
| │   │   │   └── `health.py`               | Health check endpoint                            |
| │   │   └── `router.py`                   | Combines all endpoints                           |
| ├── `core/`                               | Core app config, startup, settings               |
| │   ├── `__init__.py`                     | Core package init                                |
| │   ├── `config.py`                       | App configuration                                |
| │   └── `logging.py`                      | Logging setup                                    |
| ├── `services/`                           | Business logic, Docling integration, etc.        |
| │   ├── `__init__.py`                     | Services package init                            |
| │   └── `docling_service.py`              | Docling business logic                           |
| ├── `models/`                             | Pydantic models (request/response schemas)       |
| │   ├── `__init__.py`                     | Models package init                              |
| │   └── `docling_models.py`               | Docling request/response schemas                 |
| ├── `main.py`                             | FastAPI app entrypoint                           |

This table summarizes the recommended modular directory structure for the project, supporting clean separation of API, business logic, and models for scalability and maintainability.