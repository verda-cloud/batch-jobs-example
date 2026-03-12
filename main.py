from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict, Any
import uvicorn
import asyncio
import time
import logging
import os

app = FastAPI()

logger = logging.getLogger("uvicorn")
logger.info("Starting the app")

_job_started = False

async def simulateWork(duration: int = 5, body: Dict[str, Any] = None):
    logger.info(f"Simulating work with duration of {duration} seconds, request payload: {body}")
    for second in range(1, duration + 1):
        await asyncio.sleep(1)
        logger.info(f"Progress: {second}/{duration} seconds elapsed")

async def _exit_process(exit_code: int) -> None:
    await asyncio.sleep(0.2)
    logger.info(f"Exiting with code {exit_code}")
    os._exit(exit_code)

@app.post("/job")
async def example_endpoint(body: Dict[str, Any] = None, duration: int = 5, failed: str = "false"):
    global _job_started

    if _job_started:
        return JSONResponse(status_code=503, content={"detail": "Server is shutting down"})
    _job_started = True

    logger.info(f"Running job with duration of {duration} seconds, will fail: {failed}")
    logger.info(f"Request payload: {body}")

    try:
        await simulateWork(duration, body)
    except Exception as e:
        message = f"Job failed due to an unexpected error: {str(e)}"
        logger.error(message)
        asyncio.create_task(_exit_process(1))
        return JSONResponse(status_code=500, content={"detail": message})

    if failed == "true" or failed == "1":
        message = "Job failed as requested via failed parameter"
        logger.error(message)
        asyncio.create_task(_exit_process(1))
        return JSONResponse(status_code=500, content={"detail": message})

    message = "Job completed successfully"
    logger.info(message)
    asyncio.create_task(_exit_process(0))
    return {"success": True, "message": message, "executionTime": duration, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
