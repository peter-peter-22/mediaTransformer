from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from src.common.response import VideoUploadResponse
from pydantic import ValidationError
import shutil
import tempfile
from src.common.format_pydantic_error import handle_pydantic_error
import ffmpeg
from src.options.video_options import VideoOptions
from src.tagging.tag_video import tag_video
import os
from pathlib import Path
from typing import List
import asyncio
from src.minio.client import minio_client

router = APIRouter()

@router.post("/")
async def upload_video(file: UploadFile = File(...), options:str=Form(...)):
    try:
        # Get and validate the options
        c=VideoOptions.model_validate_json(options)
        print("Options: ",c)

        # Get file extension
        if file.filename is None:
            raise HTTPException(status_code=422, detail="File name is required")
        ext = Path(file.filename).suffix
        print("Extension: ",ext)

        # Create a temporary path for the uploaded video
        upload=tempfile.NamedTemporaryFile(delete=False,suffix=ext)
        upload_path = upload.name 
        print("Upload Path: ",upload_path)
        try:
            # Place the video to a temp path
            shutil.copyfileobj(file.file, upload)

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
            
            # Create a temporary path for the transformed video
            output_ext=c.convertTo or ext
            output=tempfile.NamedTemporaryFile(delete=False,suffix=output_ext)
            output_path=output.name
            print("Output Path: ",output_path)
            try:
                # Define mpeg settings
                fm_config={
                    "vf":c.ffmpeg_settings and c.ffmpeg_settings.vf or \
                        f"scale='min({c.limit_resolution.x},iw)':'min({c.limit_resolution.y},ih)':force_original_aspect_ratio=decrease:force_divisible_by=2:flags=bicubic" \
                        if c.limit_resolution else None,
                    "vcodec":c.ffmpeg_settings and c.ffmpeg_settings.vcodec or \
                        'libx264',
                    "acodec":c.ffmpeg_settings and c.ffmpeg_settings.acodec or \
                        'aac',
                    "format":c.convertTo,
                    "bitrate":c.bitrate,
                    "loglevel":"quiet"
                }

                # Transform the file in mpeg
                print("Transforming video",flush=True)
                (
                    ffmpeg
                    .input(upload_path)
                    .output(
                        output_path,
                        **{k: v for k, v in fm_config.items() if v is not None} # Remove None args to avoid errors
                    )
                    .overwrite_output()
                    .run(cmd="D:/ffmpeg/ffmpeg-2025-05-15-git-12b853530a-essentials_build/bin/ffmpeg.exe")
                )

                # Tag if necessary
                tags:List[str]=[]
                #test=tag_video(output_path)
                    

                # Upload
                return
                file_size = os.path.getsize(output_path)
                with open(output_path, 'rb') as data_to_upload:
                    await asyncio.to_thread(
                        lambda: minio_client.put_object(
                            c.bucket_name,
                            c.object_name,
                            data=data_to_upload,
                            length=file_size,
                            content_type=c.upload_mime_type
                        )
                    )

                # Return the response
                return VideoUploadResponse.model_construct(
                    object_name=c.object_name,
                    bucket_name=c.bucket_name, 
                    mime_type=c.upload_mime_type,
                    tags=tags
                )

            except Exception as e:
                print(e)
                raise e
            finally:
                # Remove the transformed file
                output.close()
                os.remove(output_path)
        except Exception as e:
            print(e)
            raise e
        finally:
            # Remove the original file
            upload.close()
            os.remove(upload_path)

    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e}")
        raise HTTPException(status_code=500, detail="Error processing video")
    except ValidationError as e:
        handle_pydantic_error(e)
    except Exception as e:
        # Handle other exceptions
        print(e)
        raise HTTPException(status_code=400, detail=str(e))