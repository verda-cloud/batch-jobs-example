# Batch Jobs Example

A simple example app for containers batch jobs
This application provides a single API endpoint that can simulate various job execution times and failure scenarios.

## Purpose

This application is specifically designed to be an example for a batch job app by:

- Simulating long-running jobs with configurable execution time
- Providing success and failure scenarios for testing job completion handling
- Generating logs during execution for monitoring and debugging

## API Endpoint

### GET /job

Executes a test job with configurable parameters.

**Query Parameters:**

- `timeout` (optional): Number of seconds to run the job. Default: 5 seconds
- `failed` (optional): Set to 'true' or '1' to simulate job failure

**Examples:**

```bash
# Run a job for 10 seconds (success)
curl -X POST "http://localhost:8000/job?timeout=10"

# Run a job for 30 seconds that will fail
curl -X POST "http://localhost:8000/job?timeout=30&failed=true"

# Run a job with default 5 second timeout
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
The endpoint will throw an error and return a 500 status code when `failed=true`.
The app process should exit with a non-zero status code

## Build and run:

```bash
docker logout ghcr.io # if image pull fails
docker build -t batch-jobs-example .
docker run -p 8000:8000 batch-jobs-example
```
