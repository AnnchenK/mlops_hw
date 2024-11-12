from app import app

import uvicorn
import os


if __name__ == "__main__":
    host = os.environ.get("ADDRESS", "0.0.0.0")
    port = int(os.environ.get("PORT", 0))
    uvicorn.run(app, host=host, port=port)
