from datetime import date
from app.models import JobStatus, JobLocation # Import the new Enum

MOCK_JOBS = [
    {
        "id": "101",
        "company_name": "TechNova Solutions",
        "role": "Frontend Engineer",
        "status": JobStatus.applied,
        "date_applied": date(2026, 8, 10),
        "location": JobLocation.remote, # Updated
        "notes": "Found via LinkedIn. Reached out to recruiter."
    },
    {
        "id": "102",
        "company_name": "Global Data Corp",
        "role": "Full Stack Developer",
        "status": JobStatus.interviewing,
        "date_applied": date(2026, 7, 28),
        "location": JobLocation.hybrid, # Updated
        "notes": "Technical round scheduled for next Tuesday."
    },
    {
        "id": "103",
        "company_name": "StartUp Inc",
        "role": "Web Developer",
        "status": JobStatus.rejected,
        "date_applied": date(2026, 7, 15),
        "location": JobLocation.on_site, # Updated
        "notes": "Ghosted after first round."
    },
    {
        "id": "104",
        "company_name": "CloudSync",
        "role": "UI/UX Developer",
        "status": JobStatus.screening,
        "date_applied": date(2026, 8, 5),
        "location": JobLocation.remote, # Updated
        "notes": "Completed initial HR phone screen."
    },
    {
        "id": "105",
        "company_name": "FinTech Secure",
        "role": "Frontend Engineer",
        "status": JobStatus.offer,
        "date_applied": date(2026, 6, 20),
        "location": JobLocation.on_site, # Updated
        "notes": "Offer received! Negotiating base salary."
    },
    {
        "id": "106",
        "company_name": "NextGen AI",
        "role": "Software Engineer",
        "status": JobStatus.applied,
        "date_applied": date(2026, 8, 11),
        "location": JobLocation.remote, # Updated
        "notes": "Applied directly on company portal."
    }
]