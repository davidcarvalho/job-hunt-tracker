<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { getDashboardMetrics, getDashboardChart } from '../services/api';

// Register the required Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

// 1. TypeScript Interfaces
interface DashboardMetrics {
  total_applications: number;
  active_processes: number;
  response_rate: number;
  upcoming_interviews: number;
}

interface ChartDataPoint {
  status: string;
  count: number;
}

// 2. State Management
const metrics = ref<DashboardMetrics | null>(null);
const isLoading = ref(true);

// Strict color mapping to match ReportView badges perfectly
const statusColors: Record<string, string> = {
  'Applied': '#1976d2',      // Blue
  'Screening': '#616161',    // Grey
  'Interviewing': '#f57c00', // Orange
  'Offer': '#388e3c',        // Green
  'Rejected': '#d32f2f'      // Red
};

// Chart data structure
const chartData = ref({
  labels: [] as string[],
  datasets: [
    {
      backgroundColor: [] as string[],
      data: [] as number[],
    },
  ],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
};

// 3. Fetch Data on Mount
onMounted(async () => {
  try {
    const [metricsRes, chartRes] = await Promise.all([
      getDashboardMetrics(),
      getDashboardChart()
    ]);

    metrics.value = metricsRes.data;

    // Transform backend array into Chart.js format
    const chartPoints: ChartDataPoint[] = chartRes.data;
    
    chartData.value.labels = chartPoints.map(p => p.status);
    chartData.value.datasets[0].data = chartPoints.map(p => p.count);
    
    // Assign the correct hex code based on the status name dynamically
    chartData.value.datasets[0].backgroundColor = chartPoints.map(
      p => statusColors[p.status] || '#cccccc' // Fallback grey
    );

  } catch (error) {
    console.error("Failed to load dashboard data:", error);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="dashboard">
    <h2>Dashboard Summary</h2>

    <div v-if="isLoading" class="loading">
      Loading data...
    </div>

    <div v-else>
      <!-- Metric Cards Grid -->
      <div class="metrics-grid">
        <div class="metric-card">
          <h3>Total Applied</h3>
          <p class="metric-value">{{ metrics?.total_applications }}</p>
        </div>
        <div class="metric-card">
          <h3>Active Processes</h3>
          <p class="metric-value">{{ metrics?.active_processes }}</p>
        </div>
        <div class="metric-card">
          <h3>Response Rate</h3>
          <p class="metric-value">{{ metrics?.response_rate }}%</p>
        </div>
        <div class="metric-card">
          <h3>Interviews</h3>
          <p class="metric-value">{{ metrics?.upcoming_interviews }}</p>
        </div>
      </div>

      <!-- Donut Chart Section -->
      <div class="chart-container">
        <h3>Application Status Breakdown</h3>
        <div class="chart-wrapper">
          <Doughnut :data="chartData" :options="chartOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 1rem 0;
}

h2 {
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  padding: 3rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.metric-card {
  background-color: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
  text-align: center;
  transition: transform 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-5px);
}

.metric-card h3 {
  margin: 0;
  font-size: 0.9rem;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.metric-value {
  margin: 0.5rem 0 0;
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.chart-container {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
}

.chart-container h3 {
  text-align: center;
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.chart-wrapper {
  position: relative;
  height: 400px;
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>