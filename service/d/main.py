from fastapi import FastAPI, HTTPException
from collections import deque
import uvicorn
import asyncio
from aiohttp import ClientSession, ClientError, ClientTimeout

app = FastAPI()

# Request buffer
request_queue = deque()
max_queue_size = 10000 # Maximum size of the request queue

# Semaphore to limit concurrent tasks
semaphore = asyncio.Semaphore(10000)  # Limit to 2000 concurrent requests

async def process_request(value: int):
    async with semaphore:
        new_value = value + 1
        timeout = ClientTimeout(total=10)  # Set timeout to 10 seconds
        async with ClientSession(timeout=timeout) as session:
            try:
                async with session.get(f'http://service-e:11004/e?value={new_value}') as response:
                    response.raise_for_status()
                    return await response.json()
            except ClientError as e:
                raise HTTPException(status_code=500, detail=str(e))

@app.get("/d")
async def b(value: int):
    if len(request_queue) >= max_queue_size:
        raise HTTPException(status_code=503, detail="Service busy, please try again later.")
    
    # Add the request to the queue
    request_queue.append(value)
    
    while request_queue:
        value = request_queue.popleft()
        for _ in range(3):  # Retry logic: try up to 3 times
            try:
                result = await process_request(value)
                if result:
                    return result
            except HTTPException as e:
                # Log the error
                print(f"Request failed with error: {e.detail}")
                await asyncio.sleep(1)  # Wait before retrying
        raise HTTPException(status_code=500, detail="Failed to process request after 3 attempts")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11003, workers=1)
