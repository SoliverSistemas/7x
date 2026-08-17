import os
from app import create_app

env_name = os.getenv('FLASK_ENV', 'dev')
app = create_app(env_name)

@app.cli.command("sync-properties")
def sync_properties_command():
    """Sync properties from Tecimob API (to be used with Cron)"""
    from app.services.sync_service import SyncService
    print("Starting synchronization...")
    result = SyncService.sync_all_properties()
    print(f"Result: {result}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
