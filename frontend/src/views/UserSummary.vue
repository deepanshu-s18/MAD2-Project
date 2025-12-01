<template>
  <div class="container py-4">
    <nav class="navbar navbar-expand-lg bg-light shadow-sm rounded mb-4 px-3 py-2">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-success">SmartParking</span>
        <div class="d-flex gap-2">
          <button class="btn btn-outline-secondary" @click="$router.push('/user')">Dashboard</button>
          <button class="btn btn-danger" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <h3 class="mb-4 text-primary">My Activity Summary</h3>

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
  name: 'UserSummary',
  components: { Bar },
  data() {
    return {
      loading: true,
      chartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'My Booking Status' }
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
        const res = await axios.get('http://127.0.0.1:5000/api/userhistory', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
        
        const history = res.data
        let active = 0
        let closed = 0
        
        history.forEach(h => {
          if (h.status === 'active') active++
          else closed++
        })
        
        this.chartData = {
          labels: ['Active', 'Completed'],
          datasets: [{
            label: 'Bookings',
            backgroundColor: ['#28a745', '#6c757d'],
            data: [active, closed]
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
