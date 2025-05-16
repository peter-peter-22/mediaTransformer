from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes
from src.routes.home import router as home_router
from src.routes.upload_image import router as upload_image_router
from src.routes.upload_video import router as upload_video_router

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
app.include_router(home_router)
app.include_router(upload_image_router,prefix="/upload_image")
app.include_router(upload_video_router,prefix="/upload_video")
