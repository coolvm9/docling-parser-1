import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from app.core.logging import setup_logging
setup_logging()

# This file is a launcher for the FastAPI application
# Use it for directly running the app with: python run.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)