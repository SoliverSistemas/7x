import os, sys
sys.path.insert(0, os.getcwd())

from app import create_app
from app.services.sync_service import SyncService

app = create_app()
with app.app_context():
    result = SyncService.sync_all_properties()
    print("Resultado:", result)
