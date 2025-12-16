# Extensible RAG Agent with Vertex AI Search

This repository provides a starting point for a Retrieval-Augmented Generation (RAG) system built on Google Cloud. It uses the Google Agent Development Kit (ADK) to create a conversational agent that can reason over unstructured data, like PDFs, indexed in Vertex AI Search.

The codebase is intended as a functional example that can be extended. It currently handles PDF ingestion and provides a basic chat interface, with `TODO` markers and challenges included to guide developers in enhancing its capabilities.

---

## Key Commands

Here is a summary of the most important commands for setting up and running the project.

### Makefile Commands
-   `make install`: Installs all project dependencies using Poetry.
-   `make infra`: A convenience command that runs all infrastructure setup steps in sequence (permissions, datastore, engine, GCS bucket).
-   `make check`: Runs linting and static type checking to ensure code quality.

### Application Commands
-   `poetry run python main.py --mode ingest`: Runs the ingestion pipeline to process raw documents and load them into Vertex AI Search.
-   `poetry run python main.py --mode chat`: Starts the interactive chat session with the RAG agent.
-   `poetry run python scripts/run_evaluation.py`: Runs the evaluation script to measure the agent's performance against a golden dataset.

---

## Optional & Repurposable Commands

The following scripts are not required for the basic workflow but can be altered or repurposed for custom use cases.

-   `make generate-data`: Generates synthetic medical records for testing. You can modify `scripts/generate_data.py` to create different types of data.
-   `poetry run python scripts/generate_golden_dataset.py`: Creates a structured evaluation dataset from the raw data. You can adapt this script to build custom datasets for measuring performance on specific tasks.

---
## Project Documentation

For detailed information, please refer to the following documents:

-   **[SETUP.md](./SETUP.md):** A comprehensive guide to install, configure, and run the project.
-   **[CHALLENGE.md](./CHALLENGE.md):** A guide for developers looking to extend the project's functionality, with specific challenges for 
-   **[INFRASTRUCTURE_SETUP.md](./INFRASTRUCTURE_SETUP.md):** A step-by-step guide to provision the necessary Google Cloud resources.
