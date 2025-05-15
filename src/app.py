from fastapi import FastAPI
from src.routes.upload_image import router as upload_router
from src.routes.home import router as home_router
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(upload_router,prefix="/upload")
