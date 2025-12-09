# Scripts

This directory contains operational scripts for setting up infrastructure and generating data.

---

## Infrastructure Setup

The infrastructure for this project requires two key components that are created by the following scripts. They must be run in order.

### 1. `create_datastore.sh`

-   **What it does:** This script provisions the foundational **Vertex AI Search Data Store**.
-   **Why it's needed:** This is the "memory" of the system where your PDF documents are stored, indexed, and made searchable. It uses the "Standard" tier, which is good for basic document discovery.

### 2. `create_enterprise_engine.py`

-   **What it does:** This script wraps the existing Data Store in an **Enterprise Edition App (Engine)**.
-   **Why it's needed:** This is the "brain" that provides the advanced features required for a RAG agent to work effectively. It unlocks the ability to extract detailed paragraphs and text chunks (`extractive_segments`) from your documents, which are then fed to the LLM.

---

## Why Both Scripts Are Necessary: Standard vs. Enterprise Search

A common challenge in building RAG bots is when the bot successfully identifies a relevant document but fails to answer specific questions about its content. This is because the search mechanism only returns high-level summaries (snippets), not the detailed text required for an LLM to truly comprehend the information.

### Standard Edition (Created by `create_datastore.sh`)

-   **Purpose:** Designed for traditional search to help users *find* relevant documents.
-   **Returned Content:** Provides basic metadata and short `snippets` (1-2 sentence summaries).
-   **Limitation for RAG:** Lacks the ability to extract substantial chunks of text (`extractive_segments`). This severely limits the LLM's capacity to answer complex questions. Our `create_datastore.sh` script sets up this foundational, but limited, resource.

### Enterprise Edition (Created by `create_enterprise_engine.py`)

-   **Purpose:** Built specifically to power generative AI applications like RAG.
-   **Returned Content:** Provides rich `extractive_segments` (relevant paragraphs) and `extractive_answers` (direct answers from the text).
-   **Benefit for RAG:** Enables the LLM to receive large, contextually relevant portions of text, allowing it to accurately answer specific questions by reasoning over the actual document content. Our `create_enterprise_engine.py` script upgrades our setup to this tier.

For an effective RAG application, the **Enterprise Edition is recommended**. It provides the native capabilities for the agent to properly reason over the content within the documents.

---

## Data Generation

### `generate_data.py`

-   **What it does:** This script generates synthetic, unstructured medical records in PDF format.
-   **Why it's needed:** It provides a simple way to create realistic "messy" data (like SOAP notes) to test the ingestion pipeline and the RAG agent's retrieval performance.
