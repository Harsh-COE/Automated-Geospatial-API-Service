from celery import Celery
from GeoJson import process_geojson

app = Celery('geojson_task', broker='redis://localhost:6379/0')

# Define the task
@app.task
def run_geojson_task():
    process_geojson()

# To run the task immediately on deployment and then every 10 seconds
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Run once immediately after deployment
    run_geojson_task.apply_async()
    # Schedule to run every 24 hours (86400 seconds) or once a day at a specific time
    
    sender.add_periodic_task(
        86400.0,  # Run every 24 hours (86400 seconds)
        run_geojson_task.s(),
        name='Run GeoJSON task every 24 hours'
    )

