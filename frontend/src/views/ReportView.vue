<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { getJobs, createJob, updateJobStatus} from '../services/api';


interface JobApplication {
  id: string;
  company_name: string;
  role: string;
  status: string;
  date_applied: string;
  location: string;
  notes: string;
}

const jobs = ref<JobApplication[]>([]);
const isLoading = ref(true);
const searchQuery = ref('');
const statusFilter = ref('');

// --- New Form State ---
const showAddForm = ref(false);
const isSubmitting = ref(false);
const newJob = ref({
  company_name: '',
  role: '',
  status: 'Applied', // Default status
  date_applied: new Date().toISOString().split('T')[0], // Today's date (YYYY-MM-DD)
  location: '',
  notes: ''
});

const fetchJobs = async () => {
  isLoading.value = true;
  try {
    const response = await getJobs(statusFilter.value || undefined, searchQuery.value || undefined);
    jobs.value = response.data;
  } catch (error) {
    console.error("Error fetching jobs:", error);
  } finally {
    isLoading.value = false;
  }
};

// --- New Submit Handler ---
const submitForm = async () => {
  isSubmitting.value = true;
  try {
    await createJob(newJob.value);
    
    // Reset form and hide it
    newJob.value = {
      company_name: '', role: '', status: 'Applied', 
      date_applied: new Date().toISOString().split('T')[0], 
      location: '', notes: ''
    };
    showAddForm.value = false;
    
    // Refresh the table data
    await fetchJobs();
  } catch (error) {
    console.error("Failed to create job", error);
    alert("Failed to add job. Check console for details.");
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(fetchJobs);
watch([searchQuery, statusFilter], fetchJobs);

const getStatusClass = (status: string) => {
  const lower = status.toLowerCase();
  if (lower === 'applied') return 'status-applied';
  if (lower === 'interviewing') return 'status-interviewing';
  if (lower === 'offer') return 'status-offer';
  if (lower === 'rejected') return 'status-rejected';
  return 'status-default';
};

const editingId = ref<string | null>(null);
const editingStatus = ref<string>('');

const startEdit = (job: JobApplication) => {
  editingId.value = job.id;
  editingStatus.value = job.status;
};

const cancelEdit = () => {
  editingId.value = null;
  editingStatus.value = '';
};

const saveEdit = async (id: string) => {
  try {
    await updateJobStatus(id, editingStatus.value);
    
    // Update the local list so we don't have to refetch everything
    const jobIndex = jobs.value.findIndex(j => j.id === id);
    if (jobIndex !== -1) {
      jobs.value[jobIndex].status = editingStatus.value;
    }
    
    // Close the edit mode
    editingId.value = null;
  } catch (error) {
    console.error("Failed to update status", error);
    alert("Failed to update status.");
  }
};
</script>

<template>
  <div class="report-view">
    <div class="header-row">
      <h2>Applications Report</h2>
      <button class="btn-primary" @click="showAddForm = !showAddForm">
        {{ showAddForm ? 'Close Form' : '+ Add Application' }}
      </button>
    </div>

    <!-- New Job Form -->
    <div v-if="showAddForm" class="add-form-panel">
      <h3>New Job Application</h3>
      <form @submit.prevent="submitForm">
        <div class="form-grid">
          <div class="form-group">
            <label>Company Name *</label>
            <input v-model="newJob.company_name" type="text" required class="form-input" />
          </div>
          <div class="form-group">
            <label>Role *</label>
            <input v-model="newJob.role" type="text" required class="form-input" />
          </div>
          <div class="form-group">
            <label>Status *</label>
            <select v-model="newJob.status" required class="form-input">
              <option value="Applied">Applied</option>
              <option value="Screening">Screening</option>
              <option value="Interviewing">Interviewing</option>
              <option value="Offer">Offer</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>
          <div class="form-group">
            <label>Date Applied *</label>
            <input v-model="newJob.date_applied" type="date" required class="form-input" />
          </div>
          <div class="form-group">
            <label>Location *</label>
            <select v-model="newJob.location" required class="form-input">
              <option value="" disabled>Select location...</option>
              <option value="Remote">Remote</option>
              <option value="On-site">On-site</option>
              <option value="Hybrid">Hybrid</option>
            </select>
          </div>
        </div>
        <div class="form-group full-width">
          <label>Notes</label>
          <input v-model="newJob.notes" type="text" class="form-input" />
        </div>
        <button type="submit" class="btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Saving...' : 'Save Application' }}
        </button>
      </form>
    </div>

    <div class="controls-panel">
      <div class="control-group">
        <label>Search Company or Role</label>
        <input v-model="searchQuery" type="text" placeholder="e.g., TechNova..." class="form-input" />
      </div>
      <div class="control-group">
        <label>Filter by Status</label>
        <select v-model="statusFilter" class="form-input">
          <option value="">All Statuses</option>
          <option value="Applied">Applied</option>
          <option value="Screening">Screening</option>
          <option value="Interviewing">Interviewing</option>
          <option value="Offer">Offer</option>
          <option value="Rejected">Rejected</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table v-if="!isLoading && jobs.length > 0">
        <thead>
          <tr>
            <th>Date Applied</th>
            <th>Company</th>
            <th>Role</th>
            <th>Location</th>
            <th>Status</th>
            <th>Actions</th> <!-- New Header -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id">
            <td>{{ job.date_applied }}</td>
            <td class="font-bold">{{ job.company_name }}</td>
            <td>{{ job.role }}</td>
            <td>{{ job.location }}</td>
            
            <!-- Status Column (Toggles between Badge and Dropdown) -->
            <td>
              <div v-if="editingId === job.id">
                <select v-model="editingStatus" class="form-input edit-select">
                  <option value="Applied">Applied</option>
                  <option value="Screening">Screening</option>
                  <option value="Interviewing">Interviewing</option>
                  <option value="Offer">Offer</option>
                  <option value="Rejected">Rejected</option>
                </select>
              </div>
              <span v-else class="badge" :class="getStatusClass(job.status)">
                {{ job.status }}
              </span>
            </td>
            
            <!-- Actions Column -->
            <td>
              <div v-if="editingId === job.id" class="action-buttons">
                <button @click="saveEdit(job.id)" class="btn-text save">Save</button>
                <button @click="cancelEdit" class="btn-text cancel">Cancel</button>
              </div>
              <button v-else @click="startEdit(job)" class="btn-text edit">
                ✎ Edit Status
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="!isLoading && jobs.length === 0" class="empty-state">No applications found.</div>
      <div v-if="isLoading" class="loading-state">Updating table...</div>
    </div>
  </div>
</template>

<style scoped>
.report-view { padding: 1rem 0; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
h2, h3 { color: #ffffff; margin: 0; }

.btn-primary {
  background-color: #42b983; color: white; border: none; padding: 0.6rem 1.2rem;
  border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.95rem;
}
.btn-primary:hover { background-color: #3aa876; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

/* New Form Styles */
.add-form-panel {
  background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;
  border: 1px solid #e9ecef;
}
.add-form-panel h3 { margin-bottom: 1rem; }
.form-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem;
}
.form-group { display: flex; flex-direction: column; }
.full-width { margin-bottom: 1.5rem; }
.form-group label { font-size: 0.85rem; font-weight: bold; color: #6c757d; margin-bottom: 0.3rem; }

.controls-panel {
  display: flex; gap: 1.5rem; margin-bottom: 2rem; background: white; padding: 1.5rem;
  border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e9ecef;
}
.control-group { display: flex; flex-direction: column; flex: 1; }
.control-group label { font-size: 0.85rem; font-weight: bold; color: #6c757d; margin-bottom: 0.5rem; }
.form-input { padding: 0.75rem; border: 1px solid #ced4da; border-radius: 6px; font-size: 1rem; width: 100%; box-sizing: border-box; }

.table-container { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e9ecef; overflow: hidden; }
table { width: 100%; border-collapse: collapse; text-align: left; }
th, td { padding: 1rem 1.5rem; border-bottom: 1px solid #e9ecef; }
th { background-color: #f8f9fa; color: #495057; font-weight: bold; }
tr:hover { background-color: #f8f9fa; }
.font-bold { font-weight: bold; color: #2c3e50; }

.badge { padding: 0.4em 0.8em; border-radius: 20px; font-size: 0.85rem; font-weight: bold; display: inline-block; }
.status-applied { background-color: #e3f2fd; color: #1976d2; }
.status-interviewing { background-color: #fff3e0; color: #f57c00; }
.status-offer { background-color: #e8f5e9; color: #388e3c; }
.status-rejected { background-color: #ffebee; color: #d32f2f; }
.status-default { background-color: #f5f5f5; color: #616161; }

.empty-state, .loading-state { text-align: center; padding: 3rem; color: #6c757d; font-style: italic; }
/* Inline Edit Styles */
.edit-select {
  padding: 0.3rem;
  font-size: 0.85rem;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-text {
  background: none;
  border: none;
  font-size: 0.85rem;
  cursor: pointer;
  font-weight: bold;
}
.btn-text:hover { text-decoration: underline; }
.btn-text.edit { color: #3498db; }
.btn-text.save { color: #388e3c; }
.btn-text.cancel { color: #d32f2f; }
</style>