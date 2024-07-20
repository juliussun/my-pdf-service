from fastapi import FastAPI, HTTPException, UploadFile, File
from api.model.base import PDFRequest
from typing import List
import os
from api.pdfmerger_alternative import pdf_merger
import logging
import magic

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
TEST_FILE_DIR = "api/test/test_files"
OUTPUT_DIR = "pdf_output"

logging.basicConfig(filename="app.log", level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.post("/upload_files")
async def upload_files(files:List[UploadFile] = File(...))->dict[str,str]:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    for file in files:
        if file.filename is None:
            raise HTTPException(status_code=400, detail="file must have a name")
        
        mime = magic.from_buffer(await file.read(1024), mime=True)
        if mime != "application/pdf":
            raise HTTPException(status_code=400, detail=f"unsupported file type: {mime}")
        file.file.seek(0)

        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())
            logger.info(f"{file.filename} has been uploaded")
    return {"message":"Files uploaded successfully!"}

@app.post("/merge_pdfs")
def merge_pdfs(request: PDFRequest)-> dict[str,str]:
    folder = request.folder or UPLOAD_DIR
    output_path = request.output_path

    logger.info(f"Received requests to merge PDFs from folder: {folder} to output path: {output_path}")

    if not os.path.exists(folder):
        logger.error(f"Folder does not exist: {folder}")
        raise HTTPException(status_code=400, detail="Folder does not exist")
    try:
        result = pdf_merger(folder, output_path)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    logger.info(f"PDFs merged successfully to {output_path}")
    return {"message":"PDF merged successfully", "output_path":result["output_path"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8110)
