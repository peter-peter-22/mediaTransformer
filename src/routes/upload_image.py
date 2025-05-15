from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from src.minio.client import minio_client
from PIL import Image
import io
from pydantic import ValidationError
from src.options.parseOptions import ImageOptions

router = APIRouter()

@router.post("/")
async def upload_image(file: UploadFile = File(...), options:str=Form(...)):
    try:
        # Get and validate the options
        parsedOptions=ImageOptions.model_validate_json(options)
        print("Options: ",parsedOptions)

        # Get the file type
        mimeType=file.content_type
        print("Mime Type: ",mimeType)

        # Validate the mimetype when necessary
        if parsedOptions.mineType:
            if parsedOptions.mineType != mimeType:
                raise HTTPException(status_code=400, detail=f"Mime type mismatch. Expected {parsedOptions.mineType}, got {mimeType}")
        
        # Get the file size
        size=file.size
        print("Size: ",size)
        if size is None:
            raise HTTPException(status_code=400, detail="File size is required")

        # Validate the file size when necessary
        if parsedOptions.maxSize:
            if size > parsedOptions.maxSize:
                raise HTTPException(status_code=400, detail=f"File size exceeds maximum allowed. Maximum size: {parsedOptions.maxSize} bytes, got: {size} bytes")
    
        # Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Convert to RGB if necessary
        if parsedOptions.rgbOnly and image.mode != "RGB":
            image = image.convert("RGB")

        # Limit max resolution if necessary
        if parsedOptions.maxResolution:
            image.thumbnail((parsedOptions.maxResolution.x,parsedOptions.maxResolution.y))

        # Convert and compress if necessary
        if parsedOptions.convertTo:
            converted = io.BytesIO()
            image.save(converted, format=parsedOptions.convertTo, quality=parsedOptions.quality)
            converted.seek(0)
            image=converted
        elif parsedOptions.quality is not None:
            raise HTTPException(status_code=400, detail=f"Quality parameter is not supported when the format is not specified.")

        # Upload processed image to MinIO
        bucket_name = "public"
        object_name = parsedOptions.objectName

        return "ok"
        minio_client.put_object(
            bucket_name,
            object_name,
            data=converted,
            length=converted.getbuffer().nbytes,
            content_type="image/webp"
        )

        return "Image uploaded and processed successfully."
    except ValidationError as e:
        # Handle validation errors
        errors=e.errors(include_context=False,include_url=False,include_input=False)
        messages=[f"-Field: {error.get("loc")[0]}, Error:{error.get("msg")}" for error in errors]
        raise HTTPException(status_code=422, detail=str(messages))
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=str(e))

