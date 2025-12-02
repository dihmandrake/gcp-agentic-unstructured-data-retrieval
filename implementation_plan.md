# implementation_plan.md

## Project Overview

**Project Name:** `nelly-hackathon-mvp`
**Description:** A Python-based skeleton for a RAG (Retrieval-Augmented Generation) system. It handles document ingestion (PDF parsing, chunking, JSON conversion), indexing into Vertex AI Search, and a Gemini-powered Agent for querying.

## Technology Stack

*   **Language:** Python 3.10+
*   **Cloud Provider:** Google Cloud Platform (Vertex AI, Vertex AI Search)
*   **Key Libraries:** `google-cloud-discoveryengine`, `vertexai`, `pypdf`, `python-dotenv`
*   **Testing:** `pytest`
*   **Style:** MVP, Modular, Type-hinted, Logged.

-----

## Phase 0: Prerequisites & Setup

### 0.1 GCP Configuration
1.  **Create a GCP Project.**
2.  **Enable APIs:**
    *   `discoveryengine.googleapis.com` (Vertex AI Search)
    *   `aiplatform.googleapis.com` (Vertex AI)
3.  **Authentication:**
    *   Install Google Cloud SDK: `gcloud auth application-default login`
    *   (Optional for Prod) Create a Service Account with `Discovery Engine Editor` and `Vertex AI User` roles.

### 0.2 Vertex AI Search Setup
1.  Go to **Agent Builder** > **Data Stores** > **Create Data Store**.
2.  Select **Structured Data** (since we are doing our own chunking).
3.  Define the schema (or use auto-detection with a sample JSON). Key fields: `content`, `source_file`, `page_number`.
4.  Create an App connected to this Data Store.
5.  Note down the `DATA_STORE_ID` and `PROJECT_ID`.

-----

## Phase 1: Environment & Configuration

### 1.1 Project Structure

Create the following directory structure:

```text
nelly-hackathon-mvp/
├── data/
│   ├── raw/                  # Place PDF files here
│   ├── processed/            # Output JSON files land here
│   └── failed/               # Files that failed processing
├── src/
│   ├── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py         # Centralized logging configuration
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── parser.py         # Extracts text and metadata from PDFs
│   │   ├── chunker.py        # Splits text into context-aware segments
│   │   └── pipeline.py       # Orchestrates Parsing -> Chunking -> JSON
│   ├── search/
│   │   ├── __init__.py
│   │   └── vertex_client.py  # Handles search queries to Vertex AI
│   └── agent/
│       ├── __init__.py
│       └── bot.py            # Gemini Agent logic with Search Tool
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py
│   └── test_search.py
├── .env.example              # Template for environment variables
├── .gitignore                # Standard Python gitignore
├── main.py                   # CLI Entry point (Ingest vs Chat)
├── README.md                 # Setup instructions
└── requirements.txt          # Dependencies
```

### 1.2 Configuration Files

**Create `.env.example`**:

```text
PROJECT_ID="your-gcp-project-id"
LOCATION="us-central1" # or "global" for some search features
DATA_STORE_ID="your-vertex-search-datastore-id"
GCP_CREDENTIALS_PATH="path/to/service-account.json" # Optional
```

**Create `requirements.txt`**:

```text
google-cloud-discoveryengine>=0.11.0
google-cloud-aiplatform>=1.38.0
pypdf>=3.17.0
python-dotenv>=1.0.0
pytest>=7.0.0
```

**Create `src/utils/logger.py`**:

*   Implement a `setup_logger(name)` function.
*   Use standard Python `logging` library.
*   Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.
*   Output to Console (StreamHandler) and optionally a file `app.log`.

-----

## Phase 2: The Ingestion Engine (Steps 1, 2, 3)

### 2.1 Document Parsing (`src/ingestion/parser.py`)

*   **Function:** `parse_pdf(file_path: str) -> Dict[str, Any]`
*   **Logic:**
    *   Use `pypdf.PdfReader`.
    *   Iterate through pages and extract text.
    *   **Enrichment:** Extract metadata (title, author, creation date, page count).
    *   **Innovation Point:** Add a TODO comment for developers to implement OCR for scanned docs later (e.g., using Google Cloud Document AI).
*   **Return:** A dictionary with `text` and `metadata`.

### 2.2 Text Chunking (`src/ingestion/chunker.py`)

*   **Function:** `chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]`
*   **Logic:**
    *   Implement a sliding window approach or use a recursive character splitter logic (split by paragraphs, then sentences).
    *   **Enrichment:** Ensure chunks don't break in the middle of a word.
    *   **Innovation Point:** Add a docstring noting this is where "Semantic Chunking" logic should be injected.

### 2.3 Conversion & Orchestration (`src/ingestion/pipeline.py`)

*   **Function:** `run_ingestion(input_dir: str, output_dir: str)`
*   **Logic:**
    1.  Glob all `.pdf` files in `input_dir`.
    2.  Loop through files:
        *   **Try/Except Block:**
            *   Call `parser.parse_pdf`.
            *   Call `chunker.chunk_text`.
            *   Format chunks into JSON structure required for Vertex AI Search (Structured Data):
                ```json
                {
                  "id": "uuid",
                  "content": "chunk_text",
                  "source_file": "filename",
                  "page_number": 1
                }
                ```
        *   **On Failure:** Move file to `data/failed/` and log error.
    3.  Save the result as `processed_data.json` (JSON Lines format) in `output_dir`.
    4.  Log progress via `src/utils/logger.py`.

-----

## Phase 3: Vertex AI Integration (Step 4)

### 3.1 Search Client (`src/search/vertex_client.py`)

*   **Class:** `VertexSearchClient`
*   **Init:** Load `PROJECT_ID`, `LOCATION`, `DATA_STORE_ID` from environment.
*   **Method:** `search(query: str) -> List[Dict]`
*   **Logic:**
    *   Initialize `discoveryengine.SearchServiceClient`.
    *   Execute a search query against the data store.
    *   **Enrichment:** Return a list of results with `snippet`, `title`, and `source_link`.
    *   Handle exceptions (e.g., store not found, quota exceeded).

-----

## Phase 4: The Agent (Step 5)

### 4.1 Gemini Agent (`src/agent/bot.py`)

*   **Class:** `RAGAgent`
*   **Init:** Initialize `vertexai` and the `GenerativeModel` (e.g., `gemini-1.5-flash`).
*   **Method:** `ask(question: str)`
*   **Logic:**
    *   **System Instruction:** Define a system prompt: "You are a helpful assistant. Use the provided context to answer questions. If the answer is not in the context, say so."
    *   **Tool Definition:** Define a Python function `retrieve_documents(query)` that wraps `VertexSearchClient.search`.
    *   **Bind Tool:** Bind this tool to the Gemini model.
    *   **Chat Session:** Start a chat session (`model.start_chat()`) to enable history.
    *   **Prompting:** Send the user's question. The model should decide to call the tool.
    *   **Execution:** Execute the tool call if requested, feed the context back to Gemini, and return the final natural language response.
    *   **Grounding:** (Optional) Use Vertex AI's built-in grounding if applicable, but for this MVP, manual tool calling gives more control.

-----

## Phase 5: Entry Point & CLI

### 5.1 Main Execution (`main.py`)

*   Use `argparse` to create two modes:
    1.  `ingest`: Runs `src/ingestion/pipeline.py`.
    2.  `chat`: Instantiates `RAGAgent` and starts a `while True` input loop for the user.
*   **Example Usage:**
    *   `python main.py --mode ingest`
    *   `python main.py --mode chat`

-----

## Phase 6: Verification & Testing

### 6.1 Unit Tests
*   `tests/test_ingestion.py`: Test `parse_pdf` with a dummy PDF. Test `chunker` with a known string.

### 6.2 Integration Tests
*   `tests/test_search.py`: Mock the Vertex AI client or run a real search (if creds available) to verify connectivity.

### 6.3 Manual Verification
1.  **Ingest:** Place a sample PDF in `data/raw`. Run `python main.py --mode ingest`. Check `data/processed/processed_data.json`.
2.  **Upload:** Manually upload the JSONL to Vertex AI Search (or automate if time permits).
3.  **Chat:** Run `python main.py --mode chat`. Ask a question about the PDF. Verify the answer cites the content.

-----

## Implementation Notes for the Developer

1.  **Environment:** Ensure you have the Google Cloud SDK installed and authenticated (`gcloud auth application-default login`).
2.  **Vertex Setup:** You must manually create a "Vertex AI Search" App and Data Store in the Google Cloud Console first. This code assumes the Data Store exists.
3.  **Import Strategy:** Use absolute imports (e.g., `from src.utils.logger import setup_logger`).
4.  **Error Handling:** Every major function should be wrapped in `try/except` blocks with logging.
5.  **Security:** Never commit `.env` or service account keys to git.