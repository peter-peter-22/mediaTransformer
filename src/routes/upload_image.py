from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from src.minio.client import minio_client
from PIL import Image
import io
from pydantic import ValidationError
from src.options.parse_options import ImageOptions, ImageVariant
from src.tagging.tag_image import tag_image
from src.common.response import UploadResponse, VariantUpload
import asyncio
from src.ocr.find_text import extract_text

router = APIRouter()

@router.post("/")
async def upload_image(file: UploadFile = File(...), options:str=Form(...)):
    try:
        # Get and validate the options
        parsed_options=ImageOptions.model_validate_json(options)
        print("Options: ",parsed_options)

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

        # Validate the mimetype when necessary
        if parsed_options.mime_type:
            if parsed_options.mime_type != mime_type:
                raise HTTPException(status_code=400, detail=f"Mime type mismatch. Expected {parsed_options.mime_type}, got {mime_type}")
        
        # Validate the file size when necessary
        if parsed_options.max_size:
            if size > parsed_options.max_size:
                raise HTTPException(status_code=400, detail=f"File size exceeds maximum allowed. Maximum size: {parsed_options.max_size} bytes, got: {size} bytes")
    
        # Read uploaded file
        contents = await file.read()
        bytes=io.BytesIO(contents)
        image = Image.open(bytes)

        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Read text if necessary
        text=extract_text(image,parsed_options.ocr_min_confidence) if parsed_options.ocr else None
        
        # Tag image if necessary
        tags=None
        if parsed_options.tag:
            tags=[tag.category for tag in await tag_image(image,parsed_options.tagging_top_k,parsed_options.tagging_min_confidence)]
        
        # Create a variant for the default entry
        parsed_options.variants.insert(
            0,
            ImageVariant.model_construct(
                object_name=parsed_options.object_name,
            )
        )

        # Process the variants
        responses=await asyncio.gather(*[
            upload_variant(parsed_options, variant, image)
            for variant in parsed_options.variants
        ])

        # Return results
        return UploadResponse.model_construct(
            tags=tags,
            text=text,
            files=responses
        )

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

async def upload_variant(parsed_options: ImageOptions,variant:ImageVariant, image: Image.Image):
    """
    Overwrite the default parameters with the variant then upload.
    Args:
        parsedOptions (ImageOptions): The options to use for the upload.
        variant (ImageVariant): The variant of the image to upload.
        image (Image.Image): The image to upload.
    """

    # Overwrite default parameters with the variant's values
    convertTo = variant.convert_to or parsed_options.convertTo
    limit_resolution = variant.limit_resolution or parsed_options.limit_resolution
    uploadMimeType = variant.upload_mime_type or parsed_options.upload_mime_type
    quality = variant.quality or parsed_options.quality
    bucketName = variant.bucket_name or parsed_options.bucket_name 

    # Limit max resolution if necessary
    if limit_resolution:
        image.thumbnail((limit_resolution.x,limit_resolution.y))

    # Convert, compress and save
    buffer = io.BytesIO()
    image.save(
        buffer, 
        format=convertTo or image.format, 
        quality=quality or 100
    )
    buffer.seek(0)
    
    # Upload
    await asyncio.to_thread(
        lambda: minio_client.put_object(
            bucketName,
            variant.object_name,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type=uploadMimeType
        )
    )

    # Return file metadata
    return VariantUpload.model_construct(
        objectName=variant.object_name,
        bucketName=bucketName, 
        mimeType=uploadMimeType
    )
