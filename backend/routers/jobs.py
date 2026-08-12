from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.mock_data import MOCK_JOBS
import uuid
from app.models import JobApplication, JobCreate, JobStatusUpdate

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("/", response_model=List[JobApplication])
def get_jobs(
        status: Optional[str] = None,
        search: Optional[str] = None
):
    filtered_jobs = MOCK_JOBS

    if status:
        filtered_jobs = [
            j for j in filtered_jobs
            if j["status"].value.lower() == status.lower()
        ]

    if search:
        search_lower = search.lower()
        filtered_jobs = [
            j for j in filtered_jobs
            if search_lower in j["company_name"].lower() or search_lower in j["role"].lower()
        ]

    return filtered_jobs


@router.post("/", response_model=JobApplication)
def create_job(job: JobCreate):
    # Convert Pydantic model to a standard dictionary
    new_job = job.model_dump()

    # Generate a random string ID
    new_job["id"] = str(uuid.uuid4())[:8]

    # Add to our mock database
    MOCK_JOBS.append(new_job)

    return new_job


@router.patch("/{job_id}/status", response_model=JobApplication)
def update_job_status(job_id: str, status_update: JobStatusUpdate):
    for job in MOCK_JOBS:
        if job["id"] == job_id:
            # Update the status using the Enum value
            job["status"] = status_update.status
            return job

    # If the loop finishes without finding the job, throw a 404 error
    raise HTTPException(status_code=404, detail="Job not found")