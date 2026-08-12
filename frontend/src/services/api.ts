import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Points to your FastAPI server
});

export const getDashboardMetrics = () => api.get('/dashboard/metrics');
export const getDashboardChart = () => api.get('/dashboard/chart');
export const getJobs = (status?: string, search?: string) => {
  return api.get('/jobs', {
    params: { status, search }
  });
};

export const createJob = (jobData: any) => api.post('/jobs', jobData);

export const updateJobStatus = (id: string, status: string) => 
  api.patch(`/jobs/${id}/status`, { status });