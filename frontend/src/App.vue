<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header class="navbar">
      <h1>Job Hunt Tracker</h1>
      <nav>
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/report">Applications Report</RouterLink>
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  font-family: Arial, sans-serif;
  color: #333;
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
}
.navbar h1 {
  margin: 0;
  font-size: 1.5rem;
}
nav a {
  color: #42b983;
  text-decoration: none;
  margin-left: 1.5rem;
  font-weight: bold;
}
nav a.router-link-active {
  color: white;
  text-decoration: underline;
}
.content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>