import sys
import os

# Add the project directory to python path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Wrap FastAPI ASGI app to WSGI
from a2wsgi import ASGIMiddleware
from app.main import app

application = ASGIMiddleware(app)
