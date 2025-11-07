# Batch Jobs Example

A simple example app for containers batch jobs.

This application provides an API endpoint that can simulate various job execution times and failure scenarios.

## Purpose

This application is specifically designed to be an example for a batch job app by:

- Simulating long-running jobs with configurable execution time
- Providing success and failure scenarios for testing job completion handling
- Exiting the process
- Generating logs during execution for monitoring and debugging
- Exposing a GET /health endpoint which is required for batch jobs

## API Endpoints

### POST /job

Executes a test job with configurable parameters.

**Query Parameters:**

- `duration` (optional): Number of seconds to run the job. Default: 5 seconds
- `failed` (optional): Set to 'true' or '1' to simulate job failure

### GET /health

A mandatory endpoint to make sure the app is running and is ready to accept a job.
Should return a 200 status code, body is ignored.

**Examples:**

```bash
# Run a job for 10 seconds (success)
curl -X POST "http://localhost:8000/job?duration=10"

# Run a job for 30 seconds that will fail
curl -X POST "http://localhost:8000/job?duration=30&failed=true"

# Run a job with default 5 second duration
curl -X POST "http://localhost:8000/job"
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Job completed successfully",
  "executionTime": 10,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Response (Failure):**
The endpoint will return a 500 status code when `failed=true`.
The app process should exit with a non-zero status code

## Request body and headers

This endpoint accepts an optional JSON body which is logged and echoed in job logs.

```bash
curl -X POST \
  "http://localhost:8000/job?duration=10" \
  -H "Content-Type: application/json" \
  -d '{"note":"hello"}'
```

## Build and run locally (docker):

```bash
docker logout ghcr.io # if image pull fails
docker build -t batch-jobs-example .
docker run -p 8000:8000 batch-jobs-example
```

## Local development (uv)

```bash
# Install uv if you don't have it
# macOS/Linux: https://docs.astral.sh/uv/getting-started/installation/

# Install dependencies and create venv from pyproject/uv.lock
uv sync

# Run the server (uses the managed venv)
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Exit behavior and logs

- The process intentionally exits after each request to model a batch job container lifecycle.
  - Success path: exits with code 0
  - Failure path (`failed=true` or `failed=1`): exits with non‑zero code (500 response + exit code 1)

## Tagging and Pushing the docker image

```bash
docker build -t batch-jobs-example:<VERSION> .
docker tag batch-jobs-example:<VERSION> ghcr.io/verda-cloud/batch-jobs-example:<VERSION>
docker push ghcr.io/verda-cloud/batch-jobs-example:<VERSION>
```
