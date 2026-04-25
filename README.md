# Agentic Invoice Processing & Validation System

An intelligent invoice processing system built with Python, Streamlit, MongoDB, AWS S3, LangGraph, and MCP Server.

---

## System Architecture

```
User Uploads Invoice (PDF)
        │
        ▼
┌─────────────────────────────────────────────────────┐
│                  Streamlit UI                        │
│  Upload PDF → View Status → Approve/Reject Dashboard │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│              LangGraph Agent Pipeline                │
│                                                      │
│  Node 1: Extract    → Parse PDF fields               │
│  Node 2: Validate   → Check rules & business logic   │
│  Node 3: Decide     → Auto approve / reject / review │
│  Node 4: Store      → MongoDB + AWS S3               │
│  Node 5: Notify     → Update status                  │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   MongoDB   │     │   AWS S3    │     │  MCP Server │
│ Store data  │     │ Store PDFs  │     │ AI queries  │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| LangGraph | Agent pipeline (extract → validate → decide → store) |
| Streamlit | UI (upload, dashboard, review) |
| MongoDB | Store invoice data and status |
| AWS S3 | Store original PDF files |
| MCP Server | Let AI query invoices via natural language |
| Groq / OpenAI | LLM for extraction and decisions |
| Cohere | Embeddings for similarity search |
| PyMuPDF | Extract text from PDF invoices |

---

## Project Structure

```
InvoiceProcessor/
│
├── .vscode/
│   ├── mcp.json                      # MCP server configuration
│   ├── settings.json                 # VS Code workspace settings
│   └── extensions.json               # Recommended extensions
│
├── config/
│   ├── __init__.py
│   └── settings.py                   # MongoDB, S3, LLM configs
│
├── agents/                           # LangGraph agents
│   ├── __init__.py
│   ├── graph.py                      # Main LangGraph pipeline
│   ├── extractor.py                  # Node 1: Extract invoice data
│   ├── validator.py                  # Node 2: Validate fields
│   ├── decision.py                   # Node 3: Approve/Reject logic
│   └── state.py                      # LangGraph state definition
│
├── services/                         # Business logic
│   ├── __init__.py
│   ├── mongodb_service.py            # MongoDB operations
│   ├── s3_service.py                 # AWS S3 operations
│   └── invoice_service.py            # Invoice processing
│
├── mcp/                              # MCP Server
│   ├── __init__.py
│   └── server.py                     # MCP tools for MongoDB
│
├── exceptions/
│   ├── __init__.py
│   └── handlers.py
│
├── logger/
│   ├── __init__.py
│   └── logging_config.py
│
├── streamlit_app/                    # UI
│   ├── pages/
│   │   ├── upload.py                 # Upload invoice page
│   │   ├── dashboard.py              # View all invoices
│   │   └── review.py                 # Manual review page
│   └── app.py                        # Main streamlit entry
│
├── tests/
│   ├── test_extractor.py
│   ├── test_validator.py
│   └── test_services.py
│
├── data/                             # Sample invoices (gitignored)
├── .env                              # Secrets (gitignored)
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## LangGraph Pipeline

### Invoice State

```python
# agents/state.py
from typing import TypedDict, Optional
from enum import Enum

class InvoiceStatus(str, Enum):
    PENDING  = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVIEW   = "needs_review"

class InvoiceState(TypedDict):
    # Input
    file_path:      str
    file_name:      str

    # Extracted fields
    invoice_number: Optional[str]
    vendor_name:    Optional[str]
    invoice_date:   Optional[str]
    due_date:       Optional[str]
    amount:         Optional[float]
    tax:            Optional[float]
    line_items:     Optional[list]

    # Validation
    is_valid:       Optional[bool]
    errors:         Optional[list]
    warnings:       Optional[list]

    # Decision
    status:         Optional[InvoiceStatus]
    reason:         Optional[str]
    confidence:     Optional[float]

    # Storage
    mongo_id:       Optional[str]
    s3_url:         Optional[str]
```

### Graph Pipeline

```python
# agents/graph.py
from langgraph.graph import StateGraph, END

def build_graph():
    graph = StateGraph(InvoiceState)

    graph.add_node("extract",  extract_invoice)
    graph.add_node("validate", validate_invoice)
    graph.add_node("decide",   decide_invoice)
    graph.add_node("store",    store_invoice)

    graph.set_entry_point("extract")
    graph.add_edge("extract",  "validate")
    graph.add_edge("validate", "decide")
    graph.add_edge("decide",   "store")
    graph.add_edge("store",    END)

    return graph.compile()
```

---

## Environment Variables

Create a `.env` file in the root directory:

```bash
# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DB_NAME=invoice_db
MONGODB_COLLECTION_NAME=invoices

# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=invoice-bucket

# LLM
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key

# App
APP_ENV=development
LOG_LEVEL=INFO
```

---

## Installation

```bash
# Install dependencies
uv add langgraph langchain langchain-groq langchain-openai
uv add streamlit pymongo boto3
uv add pymupdf python-dotenv pyyaml
uv add pytest structlog
```

---

## MCP Configuration

```json
// .vscode/mcp.json
{
  "servers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "${env:MONGODB_URI}"
      }
    }
  }
}
```

---

## Build Order

| Step | File | Description |
|---|---|---|
| 1 | `config/settings.py` | Centralized config |
| 2 | `agents/state.py` | Define invoice state |
| 3 | `agents/extractor.py` | Extract PDF fields with LLM |
| 4 | `agents/validator.py` | Validate business rules |
| 5 | `agents/decision.py` | Auto approve / reject |
| 6 | `agents/graph.py` | Wire up LangGraph |
| 7 | `services/mongodb_service.py` | Store results |
| 8 | `services/s3_service.py` | Upload PDFs |
| 9 | `streamlit_app/app.py` | Build UI |
| 10 | `mcp/server.py` | MCP tools |

---

## Running the App

```bash
# Run Streamlit UI
streamlit run streamlit_app/app.py

# Run tests
pytest tests/
```

---

## What the App Does

- Extract data from PDF invoices using LLM
- Validate invoice fields (amount, date, vendor)
- Store invoices in MongoDB
- Upload invoices to AWS S3
- Auto approve / reject invoices based on business rules
- Query invoices via natural language using MCP

---

## Node.js Requirement

MCP Server requires Node.js v20.19.0 or later.

```bash
node --version   # must be v20.19+
npx --version    # comes with Node.js
```
