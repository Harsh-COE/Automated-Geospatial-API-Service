import json
import os
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, ValidationError
from typing import List

# Database connection setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:admin@db:5432/karnataka_db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()

# Pydantic model for a tile
class Tile(BaseModel):
    id: int
    geometry: dict  # GeoJSON format

    class Config:
        arbitrary_types_allowed = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# READ: Retrieve tiles (list)
@app.get("/tiles/", response_model=List[Tile])
def get_tiles(db: Session = Depends(get_db)):
    query = text("""
        SELECT id, ST_AsGeoJSON(geometry) AS geometry 
        FROM karnataka_tiles
    """)
    
    result = db.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Tiles not found")
    
    tiles = [Tile(id=row[0], geometry=json.loads(row[1])) for row in rows]
    return tiles

# READ: Retrieve a specific tile by ID
@app.get("/tiles/{tile_id}", response_model=Tile)
def get_tile(tile_id: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT id, ST_AsGeoJSON(geometry) AS geometry
        FROM karnataka_tiles
        WHERE id = :tile_id
    """)
    
    result = db.execute(query, {"tile_id": tile_id})
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Tile not found")
    
    return Tile(id=row[0], geometry=json.loads(row[1]))

# CREATE: Insert new tiles (supports batch insert)
@app.post("/tiles/", response_model=List[Tile], status_code=status.HTTP_201_CREATED)
def create_tiles(tiles: List[Tile], db: Session = Depends(get_db)):
    try:
        inserted_tiles = []
        for tile in tiles:
            insert_query = text("""
                INSERT INTO karnataka_tiles (id, geometry)
                VALUES (:id, ST_SetSRID(ST_GeomFromGeoJSON(:geometry), 4326))
                RETURNING id, ST_AsGeoJSON(geometry) AS geometry
            """)
            
            result = db.execute(insert_query, {"id": tile.id, "geometry": json.dumps(tile.geometry)})
            inserted_row = result.fetchone()
            if not inserted_row:
                raise HTTPException(status_code=400, detail="Tile could not be inserted.")
            
            inserted_tile = Tile(id=inserted_row[0], geometry=json.loads(inserted_row[1]))
            inserted_tiles.append(inserted_tile)
        
        db.commit()  # Commit only after all inserts succeed
        return inserted_tiles
    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of failure
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# UPDATE: Update tiles (supports batch update)
@app.put("/tiles/", response_model=List[Tile])
def update_tiles(tiles: List[Tile], db: Session = Depends(get_db)):
    updated_tiles = []
    try:
        for tile in tiles:
            # Check if the tile exists
            check_query = text("""
                SELECT id FROM karnataka_tiles WHERE id = :tile_id
            """)
            result = db.execute(check_query, {"tile_id": tile.id})
            if not result.fetchone():
                raise HTTPException(status_code=404, detail=f"Tile with id {tile.id} not found")
            
            # Update the tile
            update_query = text("""
                UPDATE karnataka_tiles
                SET geometry = ST_SetSRID(ST_GeomFromGeoJSON(:geometry), 4326)
                WHERE id = :tile_id
                RETURNING id, ST_AsGeoJSON(geometry) AS geometry
            """)
            result = db.execute(update_query, {"tile_id": tile.id, "geometry": json.dumps(tile.geometry)})
            updated_row = result.fetchone()
            if not updated_row:
                raise HTTPException(status_code=500, detail="Tile update failed")
            
            updated_tiles.append(Tile(id=updated_row[0], geometry=json.loads(updated_row[1])))

        db.commit()  # Commit all updates together
        return updated_tiles
    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of failure
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# DELETE: Delete tiles (supports batch delete)
@app.delete("/tiles/", status_code=status.HTTP_200_OK)
def delete_tiles(tile_ids: List[int], db: Session = Depends(get_db)):
    try:
        delete_query = text("""
            DELETE FROM karnataka_tiles
            WHERE id = ANY(:tile_ids)
            RETURNING id
        """)
        result = db.execute(delete_query, {"tile_ids": tile_ids})
        deleted_ids = [row[0] for row in result.fetchall()]
        
        db.commit()  # Commit after all deletions succeed
        return {"detail": f"{len(deleted_ids)} tiles deleted successfully", "deleted_ids": deleted_ids}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
