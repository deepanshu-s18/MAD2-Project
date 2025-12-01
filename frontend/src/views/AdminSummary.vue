<template>
  <div class="container py-4">
    <nav class="navbar navbar-expand-lg bg-light shadow-sm rounded mb-4 px-3 py-2">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-primary">Admin Panel</span>
        <div class="d-flex gap-2">
          <button class="btn btn-outline-secondary" @click="$router.push('/admin')">Dashboard</button>
          <button class="btn btn-danger" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <h3 class="mb-4 text-primary">System Overview</h3>

    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card bg-primary text-white p-3">
          <h5>Total Locations</h5>
          <h3>{{ stats.total_lots || 0 }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-success text-white p-3">
          <h5>Total Spots</h5>
          <h3>{{ stats.total_spots || 0 }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-warning text-dark p-3">
          <h5>Available Spots</h5>
          <h3>{{ stats.available_spots || 0 }}</h3>
        </div>
      </div>
    </div>

    <div class="card shadow-sm p-4">
      <div v-if="loading" class="text-center">Loading chart...</div>
      <div v-else class="chart-wrapper">
        <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import axios from 'axios'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'AdminSummary',
  components: { Bar },
  data() {
    return {
      loading: true,
      stats: {},
      chartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          title: { display: true, text: 'Parking Statistics' }
        }
      }
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/parking-summary', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
        
        this.stats = res.data
        
        this.chartData = {
          labels: ['Total Lots', 'Total Spots', 'Available', 'Occupied'],
          datasets: [{
            label: 'Count',
            backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545'],
            data: [
              this.stats.total_lots, 
              this.stats.total_spots, 
              this.stats.available_spots,
              this.stats.occupied_spots
            ]
          }]
        }
        this.loading = false
      } catch (err) {
        console.error(err)
        this.loading = false
      }
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.chart-wrapper {
  height: 400px;
}
</style>
