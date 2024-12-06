import requests
import geopandas as gpd
from sqlalchemy import create_engine
import tempfile

def process_geojson():
    geojson_url = 'https://karnatkageodata.blob.core.windows.net/staging/karnatkatest.geojson'

    # Fetch GeoJSON
    try:
        response = requests.get(geojson_url, timeout=30)
        response.raise_for_status()
        print("Successfully fetched GeoJSON from the URL.")
    except requests.RequestException as e:
        print(f"Error fetching GeoJSON: {e}")
        return

    # Create a temporary file to store the downloaded GeoJSON
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.geojson') as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name
        print(f"GeoJSON file saved to temporary path: {tmp_file_path}")
    except Exception as e:
        print(f"Error saving GeoJSON to temporary file: {e}")
        return

    # Read GeoJSON into a GeoDataFrame
    try:
        gdf = gpd.read_file(tmp_file_path)
        gdf['id'] = range(1, len(gdf) + 1)
        print("GeoJSON successfully loaded into GeoDataFrame.")
    except Exception as e:
        print(f"Error reading GeoJSON into GeoDataFrame: {e}")
        return

    # Create connection to PostgreSQL database
    try:
        engine = create_engine('postgresql://admin:admin@db:5432/karnataka_db')
        connection = engine.connect()
        print("Successfully connected to the PostgreSQL database.")
    except Exception as e:
        print(f"Database connection failed: {e}")
        return

    # Write GeoDataFrame to database in chunks with commit/rollback
    chunk_size = 1000
    try:
        with connection.begin() as transaction:
            for i in range(0, len(gdf), chunk_size):
                chunk = gdf.iloc[i:i+chunk_size]
                print(f"Processing chunk {i // chunk_size + 1}: rows {i} to {i+len(chunk)-1}.")
                try:
                    chunk.to_postgis(name='karnataka_tiles', con=engine, if_exists='append' if i > 0 else 'replace', index=False)
                    print(f"Chunk {i // chunk_size + 1} successfully written to database.")
                except Exception as e:
                    print(f"Error writing chunk {i // chunk_size + 1} to database: {e}")
                    transaction.rollback()
                    print("Transaction rolled back.")
                    raise
    except Exception as e:
        print(f"Transaction failed: {e}")
    finally:
        connection.close()
        print("Database connection closed.")
