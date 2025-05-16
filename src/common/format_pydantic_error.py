from pydantic import ValidationError
from fastapi import HTTPException

def handle_pydantic_error(e:ValidationError):
    """Create readable error messages for pydantic validation errors."""
    errors=e.errors(include_context=False,include_url=False,include_input=False)
    messages=[
        f"-Field: {error.get("loc")[0]}, Error:{error.get("msg")}"
        if len(error.get("loc"))>0 else
        f"Error:{error.get("msg")}"
        for error in errors]
    raise HTTPException(status_code=422, detail=str(messages))
