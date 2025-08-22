import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pipeline

app = FastAPI(
    title="Document Audit API",
    description="API for auditing documents and extracting claims",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Document Audit API", "version": "1.0.0"}

@app.get("/status")
def status():
    return {"status": "ok", "message": "Server is running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Analyze an uploaded document and extract claims with evidence evaluation.
    
    Args:
        file: Uploaded document (PDF or text file)
        
    Returns:
        JSON response with audit results
    """
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.txt']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process the file
            result = pipeline.run_pipeline(temp_file_path)
            return JSONResponse(content=result, status_code=200)
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)