<template>
  <div class="container py-4">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-light shadow-sm rounded mb-4 px-3 py-2 sticky-top" style="top: 0; z-index: 1020;">
      <div class="container-fluid d-flex flex-wrap align-items-center gap-2">
        <span class="navbar-brand fw-bold text-success me-3">SmartParking</span>

        <input
          v-model="searchQuery"
          @keyup.enter="fetchLocations"
          class="form-control w-auto flex-grow-1"
          placeholder="Search location..."
        />

        <div class="d-flex gap-2 flex-wrap">
          <button class="btn btn-success" @click="fetchLocations">Search</button>
          <button class="btn btn-outline-primary" @click="exportData">Report</button>
          <button class="btn btn-outline-info" @click="goToSummary">Summary</button>
        </div>

        <button class="btn btn-danger ms-auto" @click="logout">Logout</button>
      </div>
    </nav>

    <!-- Selected Location Info & Spots -->
    <div v-if="selectedLocation" class="mb-5">
      <h5 class="mb-3 border-bottom pb-2 text-primary fw-bold">
        Your Search Result ::: - > 
        {{ selectedLocation.name }} - {{ selectedLocation.address }}
      </h5>
      <div class="row g-3">
        <div
          v-for="space in selectedLocation.spaces"
          :key="space.id"
          class="col-6 col-sm-4 col-md-3 col-lg-2"
        >
          <div
            :class="['p-3 text-center rounded text-white fw-bold cursor-pointer shadow-sm', space.status === 'available' ? 'bg-success' : 'bg-danger']"
            style="cursor: pointer;"
            @click="handleSpaceClick(space)"
          >
            Spot {{ space.id }}
          </div>
        </div>
      </div>
    </div>

    <!-- History Section -->
    <div class="card shadow-sm">
      <div class="card-body">
        <template v-if="userHistory.length">
          <h4 class="mb-3 text-success">My Parking History</h4>
          <div class="table-responsive">
            <table class="table table-bordered align-middle">
              <thead class="table-light">
                <tr>
                  <th>Spot</th>
                  <th>Vehicle No</th>
                  <th>Booked At</th>
                  <th>Exit Time</th>
                  <th>Status</th>
                  <th>Parking Cost</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="record in userHistory"
                  :key="record.id"
                >
                  <td>Spot {{ record.spot_id }}</td>
                  <td>{{ record.vehicle_number }}</td>
                  <td>{{ record.parking_time }}</td>
                  <td>{{ record.leaving_time || '—' }}</td>
                  <td>
                    <span :class="['badge', record.status === 'active' ? 'badge-active' : 'badge-closed']">
                      {{ record.status.charAt(0).toUpperCase() + record.status.slice(1) }}
                    </span>
                  </td>
                  <td>
                    ₹ {{ record.parking_cost !== null ? record.parking_cost : '—' }}
                  </td>
                  <td>
                    <button
                      v-if="record.status === 'active'"
                      class="btn btn-sm btn-danger"
                      @click="releaseSpace(record.id)"
                    >
                      Release
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>

        <template v-else>
          <div class="text-center py-5">
            <h4 class="text-muted mb-2">No Parking History 🚗</h4>
            <p class="text-secondary">You haven’t booked any parking spots yet. Use the search above to find one!</p>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserPanel',
  data() {
    return {
      searchQuery: '',
      selectedLocation: null,
      userHistory: []
    }
  },
  mounted() {
    this.fetchUserHistory()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },
    async fetchSpacesForLocation(locationId) {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/parkinglot/${locationId}/spots`, {
          headers: this.getHeaders()
        })
        // Ensure reactivity
        this.selectedLocation = { ...this.selectedLocation, spaces: res.data }
      } catch (err) {
        console.error('Error fetching spaces:', err)
        this.selectedLocation.spaces = []
      }
    },
    async fetchLocations() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/parkinglot', {
          headers: this.getHeaders()
        })

        const data = res.data
        if (data.parking_lots && data.parking_lots.length) {
          const query = this.searchQuery.toLowerCase().trim()
          const match = data.parking_lots.find(loc =>
            loc.name.toLowerCase().trim().includes(query)
          )

          if (match) {
            this.selectedLocation = match
            await this.fetchSpacesForLocation(match.id)
          } else {
            alert('No matching parking lot found.')
          }
        } else {
          alert('Failed to fetch parking lots.')
        }
      } catch (err) {
        console.error('Error fetching locations:', err)
        alert('Something went wrong while fetching parking lots.')
      }
    },
    async handleSpaceClick(space) {
      if (space.status !== 'available') return

      const vehicleNumber = prompt('Enter your vehicle number:')
      if (!vehicleNumber) return

      try {
        await axios.post('http://127.0.0.1:5000/api/history', {
          spot_id: space.id,
          vehicle_number: vehicleNumber
        }, { headers: this.getHeaders() })

        alert('Spot booked successfully!')
        this.fetchLocations() // Refresh spots
        this.fetchUserHistory() // Refresh history
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to book spot')
      }
    },
    async fetchUserHistory() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/userhistory', {
          headers: this.getHeaders()
        })
        this.userHistory = res.data
      } catch (err) {
        console.error('Error fetching history:', err)
      }
    },
    async releaseSpace(historyId) {
      try {
        const res = await axios.put('http://127.0.0.1:5000/api/history', {
          history_id: historyId
        }, { headers: this.getHeaders() })

        alert('Spot released successfully!')
        if (this.selectedLocation) {
          this.fetchLocations() // Refresh spots if a location is selected
        }
        this.fetchUserHistory()
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to release spot')
      }
    },
    async exportData() {
      try {
        await axios.get('http://127.0.0.1:5000/api/export-data', {
          headers: this.getHeaders()
        })
        alert('Report Sent to your email')
      } catch (err) {
        alert('Failed to generate report')
      }
    },
    goToSummary() {
      this.$router.push('/user/summary')
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.badge-active {
  background-color: #d1f0d1;
  color: #2e7d32;
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 12px;
}
.badge-closed {
  background-color: #f1f1f1;
  color: #6c757d;
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 12px;
}
</style>
