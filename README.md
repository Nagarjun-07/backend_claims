# Document Audit API

A FastAPI-based service for auditing documents and extracting verifiable claims with evidence evaluation.

## Features

- Document processing (PDF and text files)
- Claim extraction using LLM
- Claim classification (Financial, Operational, Legal & Compliance, ESG)
- Evidence retrieval from web sources and research papers
- Claim verification and evaluation
## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openrouter_api_key
   OPENROUTER_API_BASE=https://openrouter.ai/api/v1
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/`
Returns basic API information.

### GET `/status`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

### POST `/analyze`
Analyzes an uploaded document and extracts claims.

**Parameters:**
- `file`: Upload file (PDF or TXT format)

**Response:**
```json
{
  "summary": {
    "total_claims": 5,
    "processing_time_seconds": 45.67,
    "document_name": "example.pdf",
    "timestamp": "2024-01-01 12:00:00"
  },
  "claims": [
    {
      "claim_text": "Example claim text",
      "category": "Financial",
      "verdict": "Confirmed",
      "evidence_summary": "Supporting evidence found",
      "verdict_reasoning": "Detailed reasoning for the verdict",
      "source_context": "Original document context",
      "metadata": {
        "source": "document.pdf",
        "source_chunk_id": 0
      }
    }
  ]
}
```

## Usage Example

```python
import requests

# Upload and analyze a document
with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    response = requests.post("http://localhost:8000/analyze", files=files)
    
if response.status_code == 200:
    result = response.json()
    print(f"Found {result['summary']['total_claims']} claims")
else:
    print(f"Error: {response.status_code}")
```

## Testing

Run the test script to verify API functionality:
```bash
python tmp_rovodev_test_api.py
```

## Error Handling

The API includes comprehensive error handling:
- File type validation
- Temporary file cleanup
- Graceful error responses
- Detailed error messages

## Supported File Types

- PDF files (`.pdf`)
- Text files (`.txt`)

## Notes

- The system downloads research papers for evidence verification
- Processing time depends on document size and claim complexity
- All temporary files are automatically cleaned up
- Audit reports are saved locally as JSON files
