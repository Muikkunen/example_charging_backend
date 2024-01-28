"""
This module provides functionality for providing an API using FastAPI and
fetching data from MongoDB database.
"""

import asyncio

from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

from config import DATABASE_NAME, DATABASE_COLLECTION, PASSWORD, USERNAME, mongo_database_url

collection = None
client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Connects to the MongoDB server and closes the connection to it
    after the application completes.
    """
    global collection
    global client

    client = AsyncIOMotorClient(
        mongo_database_url,
        username=USERNAME,
        password=PASSWORD
    )
    # Select the database and collection
    db = client[DATABASE_NAME]
    collection = db[DATABASE_COLLECTION]
    yield
    # Close connection to the database
    client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/measurements/all", response_model=list[dict])
async def get_measurements():
    """
    Handler for the GET request to retrieve all measurements.

    Retrieves measurements from the MongoDB database.
    The data in the database is expected to consist solely of measurements
    and they are expected to be valid data.
    """
    # TODO: In future - load to pydantic object and verify data
    return await read_from_mongo()

async def read_from_mongo() -> list[dict]:
    """
    Returns the entire MongoDB collection.
    """
    global collection
    # Query the collection asynchronously
    cursor = collection.find({}, {"_id":0, "session_id":0})

    data = []
    async for document in cursor:
        # Process each document asynchronously
        data.append(document)
    return data
