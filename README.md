# Resume Parser Service 📑

[Part of Resume Flow Ecosystem](..)

The **Resume Parser Service** is an intelligent extraction engine that converts unstructured PDF resumes into structured JSON data. It serves as the bridge between legacy documents and the modern Resume Flow builder.

---

## 🚀 Service Role

This service specializes in:
- **High-Fidelity Extraction**: Using PyMuPDF to extract text while preserving content relationships.
- **LLM-Powered Mapping**: Leveraging `Llama-3.1-8B-Instruct` to interpret resume sections (Experience, Education, Skills, etc.) and map them to a strictly validated JSON schema.
- **Frontend Compatibility**: Directly outputting data in the `ResumeData` format consumed by the React UI.

---

## 🏗️ Architecture Pipeline

The extraction process follows a four-stage pipeline:

1.  **Ingestion**: Receives a PDF file via a multipart POST request.
2.  **Text Extraction**: Uses **PyMuPDF (fitz)** to extract raw text from the document.
3.  **Semantic Mapping**: The raw text is sent to the **HuggingFace Inference API** where `Llama-3.1-8B-Instruct` identifies sections and entities.
4.  **Schema Normalization**: The LLM output is parsed and normalized into the standard `ResumeData` JSON structure.

---

## 🛠️ Tech Stack

- ![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54) **Python 3.9+**
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi) **FastAPI** for high-performance API routing.
- **PyMuPDF (fitz)** for robust PDF text extraction.
- **HuggingFace Inference API** (`Llama-3.1-8B-Instruct`) for semantic understanding.

---

## 📖 API Reference

### Parse Resume
`POST /api/v1/resume/parse`

**Content-Type**: `multipart/form-data`

| Field | Type | Description |
| :--- | :--- | :--- |
| `file` | `File` | The PDF resume file to parse (Max 10MB). |

**Response (Success)**:
```json
{
  "success": true,
  "data": {
    "personalInfo": { ... },
    "workExperience": [ ... ],
    "education": [ ... ],
    "skills": [ ... ],
    "projects": [ ... ]
  }
}
```

---

## 🔧 Local Setup

### 1. Installation
Ensure you have [uv](https://docs.astral.sh/uv/) installed.

```bash
# Navigate to the service directory
cd resume-flow-ai

# Install dependencies and create a virtual environment
uv sync
```

### 2. Environment Configuration
Create a `.env` file in the root directory:

```env
HF_TOKEN=your_huggingface_token_here
```

### 3. Running the Service
```bash
uv run uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. You can explore the interactive documentation at `http://localhost:8000/docs`.

