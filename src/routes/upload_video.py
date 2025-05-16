import src.tagging.tag_video
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from src.common.response import UploadResponse, VariantUpload
from pydantic import ValidationError
from src.options.parse_options import ImageOptions, ImageVariant

router = APIRouter()

@router.post("/")
async def upload_image(file: UploadFile = File(...), options:str=Form(...)):
    try:
        # Get and validate the options
        #parsed_options=ImageOptions.model_validate_json(options)
        #print("Options: ",parsed_options)

        # Get the file type
        mime_type=file.content_type
        print("Mime Type: ",mime_type)
        if mime_type is None:
            raise HTTPException(status_code=400, detail="Mime type is required")

        # Get the file size
        size=file.size
        print("Size: ",size)
        if size is None:
            raise HTTPException(status_code=400, detail="File size is required")
        

    except ValidationError as e:
        # Handle validation errors
        errors=e.errors(include_context=False,include_url=False,include_input=False)
        messages=[
            f"-Field: {error.get("loc")[0]}, Error:{error.get("msg")}"
            if len(error.get("loc"))>0 else
            f"Error:{error.get("msg")}"
            for error in errors]
        raise HTTPException(status_code=422, detail=str(messages))
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=400, detail=str(e))