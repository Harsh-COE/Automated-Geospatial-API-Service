from celery import Celery
from GeoJson import process_geojson 

app = Celery('geojson_task', broker='redis://localhost:6379/0')

# Define the task
@app.task
def run_geojson_task():
    process_geojson()  

# To run the task immediately on deployment and seeting up daily cron job
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    run_geojson_task.apply_async()
    
    sender.add_periodic_task(86400.0, run_geojson_task.s(), name='Run GeoJSON task every 24 hours')
