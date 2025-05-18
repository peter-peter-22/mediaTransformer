from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes
from src.routes.home import router as home
from src.routes.signed_upload import router as signed_upload
from src.routes.create_upload_key import router as create_upload_key
from src.routes.upload import router as upload

# Create app
app = FastAPI()

# Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Routes
app.include_router(home)
app.include_router(upload,prefix="/upload")
app.include_router(create_upload_key,prefix="/sign")
app.include_router(signed_upload,prefix="/signed_upload")
