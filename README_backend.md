Backend README

This project includes a simple Flask backend to store uploaded documents and seed reference files.

Quick start (Windows):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install requirements

```powershell
pip install -r requirements.txt
```

3. Start the server

```powershell
python server.py
```

The backend runs on http://127.0.0.1:5050

Endpoints:
- POST /api/upload  -> multipart form field `file` to upload a document (saves file and metadata to SQLite DB)
- GET  /api/documents -> list stored documents
- POST /api/reference/seed -> seed `reference_files/` into DB as references

Seeding:
- Place reference documents in `reference_files/` and run:

```powershell
python scripts\seed_references.py
```

Or call the endpoint directly:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:5050/api/reference/seed
```
