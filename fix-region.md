The error "400 Incorrect API endpoint used. The current endpoint can only serve traffic from "global" region, but got "us-central1" region from the API request" indicates a mismatch in how your application is interacting with the Discovery Engine API.

Here's the breakdown:

1.  **Discovery Engine Locations:** Vertex AI Search (which uses the Discovery Engine API) does not use standard single cloud regions like `us-central1` in its resource paths for API calls. Instead, it uses specific multi-regions or a global endpoint:
    *   `global`: For resources not confined to a specific multi-region. The endpoint is `discoveryengine.googleapis.com`.
    *   `us`: A multi-region covering the United States. The endpoint is `us-discoveryengine.googleapis.com`.
    *   `eu`: A multi-region covering the European Union. The endpoint is `eu-discoveryengine.googleapis.com`.

2.  **The Error Cause:** Your application is sending a request that includes `locations/us-central1` in the resource name (e.g., within `serving_config`). However, the API call is being routed to an endpoint that only serves "global" traffic. This happens if:
    *   The `SearchServiceClient` is initialized without a specific regional endpoint (defaulting to global).
    *   Even if a regional endpoint *was* set, it wasn't one of the valid Discovery Engine multi-regions (`us` or `eu`), or it didn't match the location in the resource path.

To fix this, you must ensure that the API endpoint and the resource paths in your requests are consistent and use one of the valid Discovery Engine locations (`global`, `us`, or `eu`). Based on your previous attempts using `us-central1`, it's most likely your Discovery Engine resources are set up in the `us` multi-region.

Modify your `src/search/vertex_client.py` as follows:

1.  **Specify the `us` Multi-Region Endpoint:** Initialize the client to connect to `us-discoveryengine.googleapis.com`.
2.  **Use `locations/us` in Resource Paths:** Ensure that the `serving_config_name` (and any other resource identifiers) uses `locations/us`.

```python
# src/search/vertex_client.py

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
import logging

class VertexSearchClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        # Vertex AI Search uses 'global', 'us', or 'eu'. Assuming 'us' based on prior errors.
        self.discovery_engine_location = "us"
        self.logger = logging.getLogger(__name__)

        # Set the API endpoint for the 'us' multi-region
        self.api_endpoint = f"{self.discovery_engine_location}-discoveryengine.googleapis.com"
        client_options = ClientOptions(api_endpoint=self.api_endpoint)

        self.logger.info(f"VertexSearchClient initializing with endpoint: {self.api_endpoint} for Discovery Engine location: {self.discovery_engine_location}")
        self.client = discoveryengine.SearchServiceClient(client_options=client_options)
        self.logger.info("VertexSearchClient initialized.")

    def search(self, query: str, data_store_id: str):
        try:
            self.logger.info(f"Performing Vertex AI Search for query '{query}' in Discovery Engine location '{self.discovery_engine_location}'")

            # Construct the serving_config_name using the CORRECT Discovery Engine location ('us').
            # Replace 'us-central1' with 'us'.
            serving_config_name = f"projects/{self.project_id}/locations/{self.discovery_engine_location}/collections/default_collection/dataStores/{data_store_id}/servingConfigs/default_search"
            self.logger.info(f"Using serving config: {serving_config_name}")

            request = discoveryengine.SearchRequest(
                serving_config=serving_config_name,
                query=query,
                page_size=10,
            )

            response = self.client.search(request)
            return response
        except Exception as e:
            self.logger.error(f"Error during Vertex AI Search for query '{query}': {e}", exc_info=True)
            raise
```

By making these changes, your client will connect to the `us` multi-regional endpoint, and your requests will correctly specify resources within the `locations/us` scope, resolving the endpoint mismatch.

### Sources:

* [Vertex AI Search locations | Google Cloud](https://cloud.google.com/generative-ai-app-builder/docs/locations)
* [Vertex AI Search locations | Google Cloud Documentation](https://docs.cloud.google.com/generative-ai-app-builder/docs/locations)
* [Understanding the Discovery Engine REST API - Cloud Platform Support](https://g3doc.corp.google.com/company/gfw/support/cloud/playbooks/vertex-ai-search/enterprise_search/discoveryengine.md)
* [Discovery Engine API](https://g3doc.corp.google.com/google/cloud/discoveryengine/README.md)
* [Discovery Engine API | Vertex AI Search | Google Cloud](https://cloud.google.com/generative-ai-app-builder/docs/reference/rpc)
* [One Platform Discovery - One Platform](https://g3doc.corp.google.com/google/g3doc/oneplatform/discovery.md)