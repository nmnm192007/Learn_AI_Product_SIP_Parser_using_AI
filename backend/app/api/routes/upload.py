from app.services.file_service import save_upload_file
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/upload")
async def upload_file(file_in: UploadFile = File(...)):

    allowed_extensions = [".txt", ".pdf", ".log"]
    if not file_in.filename.endswith(tuple(allowed_extensions)):
        raise HTTPException(status_code=400, detail="Unsupported File Type")

    saved_path = await save_upload_file(file_in)
    return {
        "message": "File Upload Successful",
        "filename": file_in.filename,
        "content_type": file_in.content_type,
        "path": str(saved_path),
    }
