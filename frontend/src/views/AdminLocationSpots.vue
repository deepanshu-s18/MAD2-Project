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

    <h3 class="mb-4 text-center">Spots in Location</h3>

    <div v-if="loading" class="text-center">Loading spots...</div>
    
    <div v-else>
      <div v-if="spaces.length === 0" class="text-center text-muted">
        No spots found for this location.
      </div>

      <div v-else class="table-responsive shadow-sm rounded">
        <table class="table table-bordered mb-0">
          <thead class="bg-light text-primary">
            <tr>
              <th>Spot ID</th>
              <th>Status</th>
              <th>Vehicle Number</th>
              <th>User ID</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="space in spaces" :key="space.id" :class="space.status === 'available' ? 'table-success' : 'table-danger'">
              <td>Spot {{ space.id }}</td>
              <td class="text-capitalize">{{ space.status }}</td>
              <td>
                <span v-if="space.status === 'occupied'">{{ getVehicleNumber(space.id) }}</span>
                <span v-else class="text-muted">—</span>
              </td>
              <td>
                <span v-if="space.status === 'occupied'">{{ getUserId(space.id) }}</span>
                <span v-else class="text-muted">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLocationSpots',
  data() {
    return {
      spaces: [],
      reservations: [],
      loading: true
    }
  },
  async mounted() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      const locId = this.$route.params.locationId
      try {
        const spaceRes = await axios.get(`http://127.0.0.1:5000/api/spots/${locId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
        this.spaces = spaceRes.data
      } catch (err) {
        console.error(err)
        alert('Failed to load spots')
      } finally {
        this.loading = false
      }
    },
    getVehicleNumber(spaceId) {
      const space = this.spaces.find(s => s.id === spaceId)
      return space?.vehicle_number || '—'
    },
    getUserId(spaceId) {
      const space = this.spaces.find(s => s.id === spaceId)
      return space?.user_id || '—'
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>
