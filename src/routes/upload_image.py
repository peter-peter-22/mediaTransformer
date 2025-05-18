from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from src.minio.client import minio_client
from PIL import Image
import io
from pydantic import ValidationError
from src.options.image_options import ImageOptions, ImageVariant
from src.tagging.tag_image import describe_image
from src.common.response import UploadResponse, VariantUpload
import asyncio
from src.common.format_pydantic_error import handle_pydantic_error
#from src.ocr.find_text import extract_text

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
            raise HTTPException(status_code=422, detail="Mime type is required")

        # Get the file size
        size=file.size
        print("Size: ",size)
        if size is None:
            raise HTTPException(status_code=422, detail="File size is required")

        # Validate the mimetype when necessary
        if parsed_options.mime_type:
            if parsed_options.mime_type != mime_type:
                raise HTTPException(status_code=422, detail=f"Mime type mismatch. Expected {parsed_options.mime_type}, got {mime_type}")
        
        # Validate the file size when necessary
        if parsed_options.max_size:
            if size > parsed_options.max_size:
                raise HTTPException(status_code=422, detail=f"File size exceeds maximum allowed. Maximum size: {parsed_options.max_size} bytes, got: {size} bytes")
    
        # Read uploaded file
        contents = await file.read()
        bytes=io.BytesIO(contents)
        image = Image.open(bytes)

        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Tag image if necessary
        label=None
        if parsed_options.describe:
            label=describe_image(image,parsed_options.prompt,parsed_options.prompt_max_tokens)

        # Skip the upload if necessary
        if parsed_options.skip_upload:
            return UploadResponse([],label=label)
    
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
            label=label,
            files=responses
        )

    except ValidationError as e:
        handle_pydantic_error(e)
    except Exception as e:
        # Handle other exceptions
        print(e)
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
    convert_to = variant.convert_to or parsed_options.convertTo
    limit_resolution = variant.limit_resolution or parsed_options.limit_resolution
    upload_mime_type = variant.upload_mime_type or parsed_options.upload_mime_type
    quality = variant.quality or parsed_options.quality
    bucket_name = variant.bucket_name or parsed_options.bucket_name 

    # Limit max resolution if necessary
    if limit_resolution:
        image.thumbnail((limit_resolution.x,limit_resolution.y))

    # Convert, compress and save
    buffer = io.BytesIO()
    image.save(
        buffer, 
        format=convert_to or image.format, 
        quality=quality or 100
    )
    buffer.seek(0)
    
    # Upload
    await asyncio.to_thread(
        lambda: minio_client.put_object(
            bucket_name,
            variant.object_name,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type=upload_mime_type
        )
    )

    # Return file metadata
    return VariantUpload.model_construct(
        object_name=variant.object_name,
        bucket_name=bucket_name, 
        mime_type=upload_mime_type
    )
