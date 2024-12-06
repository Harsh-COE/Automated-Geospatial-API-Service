# Automated-Geospatial-API-Service

## Objective

 An automated pipeline to ingest geospatial data from GeoJSON files into a PostgreSQL database with PostGIS extensions and provide CRUD operations using a FastAPI-based API.

## Features

### 1. Data Ingestion Pipeline
   
    Fetched GeoJSON data from Azure Data Lake Storege.
    
    Transformed coordinates into a standardized spatial reference system (e.g., EPSG:4326).
    
    Inserted the data into a PostGIS-enabled PostgreSQL database.

### 2. API Development

    Developed a FastAPI-based service to handle CRUD operations on the geospatial data.

    Insert, Update and Delete APIs support bulk insertion, bulk updation and bulk deletion respectively.

    Added Validation checks and Error logs along with rollback features.


### 3. Cron Job / task Automation

    Enabled Automated Data ingestion pipeline to fetch the data using Celery and Redis.

### 4. Continerization

    Used Docker to orchestrate the containers for PostgreSQL (with PostGIS), FastAPI, Celery and Redis.

## Prerequisites

 - Docker : <https://docs.docker.com/engine/install/>
 - Docker Compose installed - <https://docs.docker.com/compose/install/linux/>

## Setup and Usage

 1. Clone the repository:
    
        git clone https://github.com/Harsh-COE/Automated-Geospatial-API-Service.git
    
        cd Automated-Geospatial-API-Service

 2. Build and start the containers:

        docker-compose up --build

3. Access the CRUD APIs using Swagger:

       http://localhost:8000/docs
   
4. To stop the containers:

       docker-compose down

## Testing

    


    

