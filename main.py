from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any
import uvicorn
import asyncio
import time
import logging
import os

app = FastAPI()

logger = logging.getLogger("uvicorn") # Get the uvicorn logger
logger.info("Starting the app")

async def simulateWork(duration: int = 5, body: Dict[str, Any] = None):
    # job logic goes here, in this example we simulate work by sleeping for the duration of the job
    logger.info(f"Simulating work with duration of {duration} seconds, request payload: {body}")

    # Simulate a "job" by sleeping for the duration of the job, logging progress every second.
    for second in range(1, duration + 1):
        await asyncio.sleep(1)
        logger.info(f"Progress: {second}/{duration} seconds elapsed")

def _exit_process(exit_code: int) -> None:
    # This function is called to exit the process after the response is sent, to finish the job.
    time.sleep(0.1) # Small delay to ensure response has flushed
    os._exit(exit_code) # Exit the process with the exit code, use os._exit instead of sys.exit to suppress ASGI application exception

@app.post("/job")
async def example_endpoint(background_tasks: BackgroundTasks, body: Dict[str, Any] = None, duration: int = 5, failed: str = "false"):
    logger.info(f"Running job with duration of {duration} seconds, will fail: {failed}")
    logger.info(f"Request payload: {body}")

    try:
        # Run the job
        await simulateWork(duration, body)
    except Exception as e:
        message = f"Job failed due to an unexpected error: {str(e)}"
        logger.error(message)
        background_tasks.add_task(_exit_process, 1) # exit after response is sent with a non-zero code to trigger a failure
        return JSONResponse(
            status_code=500,
            content={"detail": message}
        )

    # The app must exit in order for the job to be considered completed
    # We add a background task to exit the app after the response is sent, otherwise the app will keep running until it hits the deadline and be considered failed
    if failed == "true" or failed == "1":
        message = "Job failed as requested via failed parameter"
        logger.error(message)
        background_tasks.add_task(_exit_process, 1) # exit after response is sent with a non-zero code to trigger a failure
        
        # Return a 500 response manually (don't raise HTTPException)
        return JSONResponse(
            status_code=500,
            content={"detail": message}
        )
    else:
        message = "Job completed successfully"
        logger.info(message)
        background_tasks.add_task(_exit_process, 0) # exit after response is sent with a zero code to trigger a success
        return {"success": True, "message": message, "executionTime": duration, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")} # optional: return a success response

# Health check endpoint is required for batch jobs
@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
