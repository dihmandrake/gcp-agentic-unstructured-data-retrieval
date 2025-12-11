# Scripts

This directory contains operational scripts for setting up infrastructure and generating data.

---

## Infrastructure Setup

The infrastructure for this project requires two key Google Cloud resources. The included `Makefile` provides a streamlined way to provision them.

### Provisioning with Make

-   **`make create-datastore`**: Provisions the Vertex AI Search Data Store.
-   **`make create-engine`**: Provisions the Enterprise Search App (Engine).
-   **`make infra`**: A convenience target that runs both in the correct order.

### Manual Execution

You can also run the scripts directly:

1.  **`./create_datastore.sh`**
    -   **What it does:** Provisions the foundational **Vertex AI Search Data Store**.
    -   **Why it's needed:** This is the "memory" of the system where your PDF documents are stored, indexed, and made searchable.

2.  **`poetry run python create_enterprise_engine.py`**
    -   **What it does:** Wraps the existing Data Store in an **Enterprise Edition App (Engine)**.
    -   **Why it's needed:** This is the "brain" that provides the advanced features required for a RAG agent to work effectively. It unlocks the ability to extract detailed paragraphs and text chunks (`extractive_segments`) from your documents, which are then fed to the LLM.

---

## Why Both Are Necessary: Standard vs. Enterprise Search

A common challenge in building RAG bots is when the bot successfully identifies a relevant document but fails to answer specific questions about its content. This is because the search mechanism only returns high-level summaries (snippets), not the detailed text required for an LLM to truly comprehend the information.

-   **Standard Edition (Data Store):** Designed for traditional search to help users *find* relevant documents. It provides basic metadata and short `snippets` but lacks the ability to extract substantial chunks of text (`extractive_segments`).
-   **Enterprise Edition (Engine/App):** Built specifically to power generative AI applications like RAG. It provides rich `extractive_segments` and `extractive_answers`, enabling the LLM to receive large, contextually relevant portions of text and accurately answer specific questions.

For an effective RAG application, the **Enterprise Edition is required**.

---

## Data Generation

### `generate_data.py`

-   **What it does:** This script generates synthetic, unstructured medical records in PDF format.
-   **Why it's needed:** It provides a simple way to create realistic "messy" data (like SOAP notes) to test the ingestion pipeline and the RAG agent's retrieval performance.
-   **How to run:**
    ```bash
    poetry run python scripts/generate_data.py
    ```
