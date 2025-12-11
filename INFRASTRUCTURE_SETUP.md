# Infrastructure Setup Guide

This guide provides instructions to provision the required Google Cloud infrastructure for this application. The setup is a two-step process that can be easily managed using the provided `Makefile`.

1.  **Create a Vertex AI Search Data Store:** This is where your unstructured documents (PDFs) will be stored and indexed.
2.  **Create an Enterprise Search App (Engine):** This sits on top of the Data Store and provides the advanced RAG capabilities (`extractive_segments`) needed by the agent.

---

## Automated Setup with `make`

The easiest way to provision your infrastructure is by using the `Makefile` commands from the root of the project.

### Instructions

1.  **Configure your environment:**
    -   Ensure your `.env` file is correctly filled out with your `PROJECT_ID`, `LOCATION`, `DATA_STORE_ID`, and `ENGINE_ID`. The setup scripts will use these values.

2.  **Authenticate with Google Cloud:**
    -   If you haven't already, run `gcloud auth application-default login`.

3.  **Run the infrastructure setup command:**
    ```bash
    make infra
    ```
    -   This command will run `make create-datastore` and `make create-engine` in the correct sequence. The process may take a few minutes to complete.

---

## Manual Setup

If you prefer to run the scripts manually, follow these steps from the project root.

### Step 1: Create the Data Store

```bash
bash scripts/create_datastore.sh
```

### Step 2: Create the Enterprise Search App

```bash
poetry run python scripts/create_enterprise_engine.py
```

---

## How It Works

The `create_datastore.sh` script provisions the foundational Data Store. The `create_enterprise_engine.py` script then wraps it with an Enterprise-tier App. This second step is crucial because it unlocks the `extractive_segments` feature, which allows the RAG agent to retrieve detailed text chunks from your documents instead of just summaries.

The application code in `src/search/vertex_client.py` is already configured to automatically detect and use the `ENGINE_ID` from your `.env` file, so no manual code changes are required after provisioning.
