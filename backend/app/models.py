from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date

class JobStatus(str, Enum):
    applied = "Applied"
    screening = "Screening"
    interviewing = "Interviewing"
    offer = "Offer"
    rejected = "Rejected"

class JobLocation(str, Enum):
    remote = "Remote"
    on_site = "On-site"
    hybrid = "Hybrid"

class JobApplication(BaseModel):
    id: str
    company_name: str
    role: str
    status: JobStatus
    date_applied: date
    location: JobLocation  # <-- Updated to enforce the Enum
    notes: Optional[str] = ""

class JobCreate(BaseModel):
    company_name: str
    role: str
    status: JobStatus
    date_applied: date
    location: JobLocation  # <-- Updated to enforce the Enum
    notes: Optional[str] = ""

class DashboardMetrics(BaseModel):
    total_applications: int
    active_processes: int
    response_rate: float
    upcoming_interviews: int

class ChartDataPoint(BaseModel):
    status: str
    count: int

class JobStatusUpdate(BaseModel):
    status: JobStatus