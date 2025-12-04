# nelly-hackathon-mvp

A Python-based skeleton for a RAG (Retrieval-Augmented Generation) system. It handles document ingestion (PDF parsing, chunking, JSON conversion), indexing into Vertex AI Search, and a Gemini-powered Agent for querying.

## Technology Stack

*   **Language:** Python 3.10+
*   **Cloud Provider:** Google Cloud Platform (Vertex AI, Vertex AI Search)
*   **Key Libraries:** `google-cloud-discoveryengine`, `vertexai`, `pypdf`, `python-dotenv`

## Development Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd gcp-agentic-unstructured-data-retrieval
    ```

2.  **Install [Poetry](https://python-poetry.org/docs/#installation):**
    Follow the instructions on the official Poetry website to install it on your system.

3.  **Install dependencies:**
    ```bash
    poetry install
    ```

4.  **Configure environment variables:**
    *   Copy the example `.env.example` file to a new `.env` file:
        ```bash
        cp .env.example .env
        ```
    *   Edit the `.env` file and add your Google Cloud project details:
        ```
        PROJECT_ID="your-gcp-project-id"
        LOCATION="us-central1"
        DATA_STORE_ID="your-vertex-search-datastore-id"
        ```

5.  **Create GCS Bucket:**
    *   Create a GCS bucket to store the processed data. Use the `gsutil mb` command, replacing `"your-gcp-project-id"` and `"your-bucket-name"` with your actual project ID and a unique bucket name:
        ```bash
        gsutil mb -p "your-gcp-project-id" gs://
        ```
    *   Add the bucket name to your `.env` file:
        ```
        GCS_BUCKET_NAME="your-bucket-name"
        ```

6.  **Authenticate with Google Cloud:**
    *   Ensure you have the [Google Cloud SDK](httpss://cloud.google.com/sdk/docs/install) installed.
    *   Enable the AI Platform and Discovery Engine services:
        ```bash
        gcloud services enable aiplatform.googleapis.com
        gcloud services enable discoveryengine.googleapis.com
        ```
    *   Log in with your application-default credentials:
        ```bash
        gcloud auth application-default login
        ```

## Usage

The application has two modes: `ingest` and `chat`.

### Ingest Mode: The GCS-Native Workflow

This mode uses a Google Cloud Storage-native approach to index your documents in Vertex AI Search. This is the recommended method for `CONTENT_REQUIRED` datastores.

1.  **Place your PDF files** into the `data/raw` directory.

2.  **Run the ingestion pipeline:**
    ```bash
    poetry run python main.py --mode ingest
    ```

#### End-to-End Ingestion Flow

Running the `ingest` command triggers the following automated process:

1.  **Upload Raw PDFs to GCS:** Each PDF file in `data/raw` is uploaded to a `raw/` directory in your configured GCS bucket.
2.  **Generate Metadata:** A `metadata.jsonl` file is created locally in the `data/processed` directory. Each line in this file is a JSON object that contains:
    *   A unique `id` for the document.
    *   A `content` object with the `mimeType` and the GCS `uri` pointing to the uploaded PDF.
3.  **Upload Metadata to GCS:** The `metadata.jsonl` file is uploaded to a `metadata/` directory in your GCS bucket.
4.  **Trigger Vertex AI Search Import:** The script makes an API call to Vertex AI Search, pointing it to the `metadata.jsonl` file on GCS. Vertex AI Search then reads this file, fetches the PDFs from GCS, and handles the parsing, chunking, and indexing internally.

### Chat Mode

This mode starts an interactive chat session with the RAG agent, allowing you to ask questions about the documents you have ingested.

```bash
poetry run python main.py --mode chat
```

## Makefile Commands

This project uses a `Makefile` to streamline common development tasks.

*   **`make install`**:
    *   Installs all project dependencies using Poetry.

*   **`make check`**:
    *   Performs a series of checks to ensure code quality and consistency:
        *   Checks for lock file consistency.
        *   Lints the code using `ruff`.
        *   Performs static type checking with `mypy`.
        *   Checks for obsolete dependencies with `deptry`.

## Testing

Once the development setup is complete, you can test the application by following these steps:

1.  **Install Dependencies:**
    If you haven't already, install the required libraries using Poetry:
    ```bash
    make install
    ```
    or
    ```bash
    poetry install
    ```

2.  **Add PDF Files:**
    Place the PDF documents you want to process into the `data/raw/` directory.

3.  **Run the Ingestion Pipeline:**
    Use the `ingest` mode to upload your PDFs to GCS and trigger the Vertex AI Search import.
    ```bash
    poetry run python main.py --mode ingest
    ```
    After the process completes, a `metadata.jsonl` file will be created in the `data/processed/` directory, and the import job will be initiated in Vertex AI Search.

4.  **Start the Chatbot:**
    Once the import is complete in the Google Cloud Console, run the `chat` mode to interact with the RAG agent. The agent will use the documents indexed in your Vertex AI Search datastore to answer questions.
    ```bash
    poetry run python main.py --mode chat
    ```
