from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import jobs, dashboard

app = FastAPI(title="Job Hunt Tracker API")

# Allow the Vue frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the routers
app.include_router(jobs.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Job Hunt Tracker API is running. Go to /docs to see the API endpoints."}