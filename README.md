# Automated-Geospatial-API-Service

## Objective

 #### An automated pipeline to ingest geospatial data from GeoJSON files into a PostgreSQL database with PostGIS extensions and provide CRUD operations using a FastAPI-based API.

## Features

### 1. Data Ingestion Pipeline
   
    Fetched GeoJSON data from Azure Data Lake Storege.
    
    Transformed coordinates into a standardized spatial reference system (e.g., EPSG:4326).
    
    Inserted the data into a PostGIS-enabled PostgreSQL database.

### 2. API Development

    Developed a FastAPI-based service to handle CRUD operations on the geospatial data.

    Insert, Update and Delete APIs support bulk insertion, bulk updation and bulk deletion respectively.

    Added Validation checks and Error logs along with rollback features.


### 3. Cron Job / Task Automation

    Enabled Automated Data ingestion pipeline to fetch the data using Celery and Redis.

### 4. Containerization

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

#### CRUD APIs can be accessed using Swagger at http://localhost:8000/docs or using Postman.

   #### 1. GET /tiles/ - exposes API endpoint to fetch all the tiles

   <img width="1136" alt="Screenshot 2024-12-07 at 12 00 34 PM" src="https://github.com/user-attachments/assets/33d76003-a6c7-4d47-a48b-9d5a43dc7a61">

   #### 2.  GET /tiles/{tile_id} - exposes API endpoint to get a specific tile

   <img width="1139" alt="Screenshot 2024-12-07 at 12 07 21 PM" src="https://github.com/user-attachments/assets/81cacd5b-c278-41fe-9725-009ecfa116d5">


   #### 3.  PUT /tiles/ - exposes API endpoint to update tiles (Supports bulk updates)

   <img width="747" alt="Screenshot 2024-12-07 at 12 11 58 PM" src="https://github.com/user-attachments/assets/7936fdcf-c357-473a-897b-25ac5c74045a">
         
   ##### Request Body Example:
         [
           {
               "id": 1,
               "geometry": {
                   "type": "Polygon",
                   "coordinates": [
                       [
                           [77.5946, 12.9716],
                           [77.5946, 12.9726],
                           [77.5956, 12.9726],
                           [77.5956, 12.9716],
                           [77.5946, 12.9716]
                       ]
                   ]
               }
           },
           {
               "id": 2,
               "geometry": {
                   "type": "Polygon",
                   "coordinates": [
                       [
                           [77.6343, 12.9711],
                           [77.6343, 12.9724],
                           [77.6353, 12.9724],
                           [77.6353, 12.9734],
                           [77.6343, 12.9711]
                       ]
                   ]
               }
           }
        ]

   #### 4. POST /tiles/ - exposes API endpoint to add tiles (Supports bulk addition)


   <img width="748" alt="Screenshot 2024-12-07 at 12 23 40 PM" src="https://github.com/user-attachments/assets/67842842-9236-47b1-a67b-682d49136506">

   ##### Request Body Example:
     
     [
           {
               "id": 101,
               "geometry": {
                   "type": "Polygon",
                   "coordinates": [
                       [
                           [77.5946, 12.9716],
                           [77.5946, 12.9726],
                           [77.5956, 12.9726],
                           [77.5956, 12.9716],
                           [77.5946, 12.9716]
                       ]
                   ]
               }
           },
           {
               "id": 102,
               "geometry": {
                   "type": "Polygon",
                   "coordinates": [
                       [
                           [77.6343, 12.9711],
                           [77.6343, 12.9724],
                           [77.6353, 12.9724],
                           [77.6353, 12.9734],
                           [77.6343, 12.9711]
                       ]
                   ]
               }
           }
        ]

  #### 5. DELETE /tiles/ - exposes API endpoint to delete tiles (Supports bulk deletion)

   <img width="1132" alt="Screenshot 2024-12-07 at 12 29 02 PM" src="https://github.com/user-attachments/assets/ffb0a6e4-9c91-4e2b-a22e-9a406d68781c">

   ##### Request Body Example:

     [1, 2, 3]


#### Create, Delete, Update APIs can be further validated using GET APIs.


## Troubleshooting

##### 1. If the database container fails to start, ensure Docker is running and that the 5432 ports are not already in use.

##### 2. Ensure that no conflicting containers exist and no leftover containers are using the same ports.

##### 3. If the FastAPI server is not reachable, confirm that the app container is running:
     docker ps
##### 4. Check the logs for detailed error messages:
    docker-compose logs         



    


    

