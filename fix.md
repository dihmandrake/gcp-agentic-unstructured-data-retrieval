# Fix: Search Client Logic Masking Data

## Issue Summary
The `VertexSearchClient` is successfully retrieving rich Enterprise data (`extractive_segments`), but the Python logic is discarding it.

* **Current Logic:** Uses `if/elif` blocks. If `extractive_answers` (short summaries) are found, the code hits the first `if` and skips the `elif` block for `extractive_segments` (detailed paragraphs).
* **Consequence:** The bot receives only 1-2 sentences of context instead of full paragraphs, leading to "I don't have enough information" responses.

## Resolution
Refactor `src/search/vertex_client.py` to use independent `if` statements. We should prioritize collecting **Segments** (best for RAG) and append **Answers** as supplementary data.

## Code Fix

Open `src/search/vertex_client.py` and replace the parsing logic loop inside the `search` method.

### Target: `src/search/vertex_client.py`

```python
<<<<
                # 1. Check for Extractive Answers (Q&A style)
                if data.get("extractive_answers"):
                    for answer in data["extractive_answers"]:
                        context_snippets.append(answer.get("content", ""))
                
                # 2. Check for Extractive Segments (Common for PDFs)
                elif data.get("extractive_segments"):
                    for segment in data["extractive_segments"]:
                        context_snippets.append(segment.get("content", ""))

                # 3. Fallback to Snippets
                elif data.get("snippets"):
                    for snippet in data["snippets"]:
                        context_snippets.append(snippet.get("snippet", ""))
====
                # 1. Collect Extractive Segments (Priority: High - contains full paragraphs)
                if data.get("extractive_segments"):
                    for segment in data["extractive_segments"]:
                        context_snippets.append(segment.get("content", ""))

                # 2. Collect Extractive Answers (Priority: Medium - specific facts)
                if data.get("extractive_answers"):
                    for answer in data["extractive_answers"]:
                        context_snippets.append(answer.get("content", ""))

                # 3. Fallback to Snippets only if no better context was found
                if not context_snippets and data.get("snippets"):
                    for snippet in data["snippets"]:
                        context_snippets.append(snippet.get("snippet", ""))
>>>>