from fastapi import APIRouter
from typing import List
from app.models import DashboardMetrics, ChartDataPoint
from app.mock_data import MOCK_JOBS

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/metrics", response_model=DashboardMetrics)
def get_metrics():
    total = len(MOCK_JOBS)

    # Calculate active processes (Applied, Screening, Interviewing)
    active_statuses = ["Applied", "Screening", "Interviewing"]
    active = sum(1 for j in MOCK_JOBS if j["status"].value in active_statuses)

    # Calculate response rate (Interviews + Offers / Total)
    positive_responses = sum(1 for j in MOCK_JOBS if j["status"].value in ["Interviewing", "Offer"])
    response_rate = (positive_responses / total) * 100 if total > 0 else 0

    # Count upcoming interviews
    upcoming = sum(1 for j in MOCK_JOBS if j["status"].value == "Interviewing")

    return DashboardMetrics(
        total_applications=total,
        active_processes=active,
        response_rate=round(response_rate, 1),
        upcoming_interviews=upcoming
    )


@router.get("/chart", response_model=List[ChartDataPoint])
def get_chart_data():
    status_counts = {}
    for j in MOCK_JOBS:
        status_name = j["status"].value
        status_counts[status_name] = status_counts.get(status_name, 0) + 1

    return [ChartDataPoint(status=k, count=v) for k, v in status_counts.items()]