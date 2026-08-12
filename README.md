# Job Hunt Tracker

A full-stack web application designed to help you track job applications, visualize your interview pipeline, and manage application statuses in real-time.

## Tech Stack

*   **Frontend:** Vue 3, TypeScript, Vite, Vue Router, Chart.js, Axios
*   **Backend:** FastAPI, Python, Pydantic
*   **Package Managers:** `pnpm` (Frontend), `uv` / `pip` (Backend)

## Features

*   **Interactive Dashboard:** Visualizes application statuses using a dynamic Donut chart.
*   **Metrics Tracking:** Calculates total applications, active processes, and upcoming interviews.
*   **Application Management:** Add new job applications with a built-in form.
*   **Inline Editing:** Quickly update the status of an existing application directly from the table.
*   **Real-time Filtering:** Search by company/role or filter by application status.
*   **Type Safety:** End-to-end validation using TypeScript interfaces and Pydantic models.

---

## Prerequisites

Before you begin, ensure you have the following installed:
*   [Node.js](https://nodejs.org/) (v18 or higher)
*   [pnpm](https://pnpm.io/installation)
*   [Python](https://www.python.org/) (v3.9 or higher)
*   [uv](https://github.com/astral-sh/uv) (Optional, but recommended for fast Python package management)

---

## Installation & Setup

This project requires running both the backend API and the frontend development server concurrently. 

### 1. Start the FastAPI Backend

Open a terminal and navigate to the `backend` directory:

```bash
cd backend
uv sync
# Run the server with auto-reload enabled
uv run uvicorn app.main:app --reload
```
The backend API will be available at http://localhost:8000
Interactive API documentation (Swagger) is available at http://localhost:8000/docs

### 2. Start the Vue Frontend
Open a new, separate terminal window, and navigate to the frontend directory:

```bash
cd frontend
# Install dependencies
pnpm install
# Start the dev server
pnpm dev
```



The frontend application will be available at http://localhost:5173

Notes on Data Storage
Currently, this application uses an in-memory mock database (MOCK_JOBS in mock_data.py) to store application data.

Adding or editing applications works perfectly while the server is running.

Restarting the FastAPI server will reset the data back to its default state.
