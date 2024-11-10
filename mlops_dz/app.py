from fastapi import FastAPI
from typing import Literal
import logging


logger = logging.getLogger("uvicorn")
app = FastAPI()


@app.get("/alive", summary="Aliveness check", response_model=Literal["yes", "no"])
async def root():
    """
      Returns "yes" if the service is alive and is ready to serve requests.
    """
    return "yes"
