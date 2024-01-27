import asyncio

from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

from config import DATABASE_URL, DATABASE_NAME, DATABASE_COLLECTION, PASSWORD, USERNAME

collection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the MongoDB server
    global collection

    #client = AsyncIOMotorClient(DATABASE_URL)
    client = AsyncIOMotorClient(
        "mongodb://localhost:27017/",
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
    # Expect that data is correct
    # TODO: In future - load to pydantic object and show in swagger
    return await read_from_mongo()

async def read_from_mongo():
    global collection
    # Query the collection asynchronously
    cursor = collection.find({}, {"_id":0, "session_id":0})

    data = []
    async for document in cursor:
        # Process each document asynchronously
        data.append(document)
    return data


#if __name__ == "__main__":
#    # Run the asynchronous function
#    asyncio.run(read_from_mongo())

#if __name__ == "__main__":
#    uvicorn.run(app, port=8000, host="0.0.0.0", reload=True)