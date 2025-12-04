Here is a bash script to create the Discovery Engine DataStore using `curl`. The script now sources its configuration from your `.env` file for better security and consistency.

```bash
#!/bin/bash

# --- Configuration ---
# Source environment variables from .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Validate that the required environment variables are set
if [ -z "${PROJECT_ID}" ] || [ -z "${LOCATION}" ] || [ -z "${DATA_STORE_ID}" ]; then
  echo "ERROR: One or more required environment variables are not set."
  echo "Please ensure PROJECT_ID, LOCATION, and DATA_STORE_ID are defined in your .env file."
  exit 1
fi

DISPLAY_NAME="Nelly Hackathon DataStore" # This can remain as a default
DEFAULT_COLLECTION="default_collection"

# --- 1. Authenticate with Google Cloud ---
echo "Ensuring gcloud is authenticated..."
if ! gcloud auth print-access-token > /dev/null 2>&1; then
  echo "You are not logged in. Please run 'gcloud auth application-default login'."
  gcloud auth application-default login
  if ! gcloud auth print-access-token > /dev/null 2>&1; then
    echo "Authentication failed. Exiting."
    exit 1
  fi
fi
echo "Authentication successful."

# --- 2. Construct the API Endpoint and URL for DataStore Creation ---
API_ENDPOINT="${LOCATION}-discoveryengine.googleapis.com"
CREATE_DS_URL="https://${API_ENDPOINT}/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/${DEFAULT_COLLECTION}/dataStores?dataStoreId=${DATA_STORE_ID}"

# --- 3. Define the DataStore Payload ---
CREATE_DS_PAYLOAD='{
  "displayName": "'"${DISPLAY_NAME}"'",
  "industryVertical": "GENERIC",
  "solutionTypes": ["SOLUTION_TYPE_SEARCH"],
  "contentConfig": "CONTENT_REQUIRED"
}'

# --- 4. Send the Request to Create the DataStore ---
echo ""
echo "--- Attempting to create Discovery Engine DataStore '${DATA_STORE_ID}' in '${LOCATION}' ---"
echo "Using Project ID: ${PROJECT_ID}"
echo "API URL: ${CREATE_DS_URL}"
echo "Payload: ${CREATE_DS_PAYLOAD}"
echo ""

CREATE_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: ${PROJECT_ID}" \
  "${CREATE_DS_URL}" \
  -d "${CREATE_DS_PAYLOAD}")

# --- 5. Check the Response ---
if echo "${CREATE_RESPONSE}" | grep -q "error"; then
  echo "ERROR: Failed to create DataStore."
  echo "${CREATE_RESPONSE}"
  if echo "${CREATE_RESPONSE}" | grep -q "already exists"; then
    echo "The DataStore '${DATA_STORE_ID}' in '${LOCATION}' already exists."
  fi
else
  echo "Successfully initiated DataStore creation."
  echo "${CREATE_RESPONSE}"
fi
```

### Explanation:

1.  **Configuration:** The script now begins by loading the `.env` file from the root of your project. It then checks to make sure that `PROJECT_ID`, `LOCATION`, and `DATA_STORE_ID` have been loaded correctly. If any are missing, it will exit with an error.

2.  **Authentication:** The script checks if you have valid application default credentials. If not, it prompts you to log in using `gcloud auth application-default login`.

3.  **API Endpoint and URL:** The script constructs the correct regional API endpoint (e.g., `eu-discoveryengine.googleapis.com`) and the full URL for the REST API call, using the variables loaded from your `.env` file.

4.  **DataStore Payload:** The JSON payload defines the properties of the DataStore, including its display name and configuration for unstructured document search.

5.  **`curl` Command for Creation:** This command sends the actual request to the Google Cloud API to create the datastore, using your authentication token and project ID.

6.  **Response Check:** The script checks the API response to see if the creation was successful or if an error occurred.

This updated script provides a more secure and robust way to create your datastore, ensuring it matches the configuration used by your Python application.