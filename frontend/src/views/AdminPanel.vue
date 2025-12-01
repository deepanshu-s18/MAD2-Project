<template>
  <div class="layout-container">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo">
        <a href="/admin">Admin Panel</a>
      </div>

      <ul class="nav-links">
        <li><a href="/admin">Dashboard</a></li>
        <li><a href="#" @click.prevent="showUsers">All Users</a></li>
        <li><a href="#" @click.prevent="showAddModal = true">Add Parking Lot</a></li>
        <li><a href="#" @click.prevent="showManage">Manage Parking Lots</a></li>
        <li><a href="#" @click.prevent="$router.push('/admin/summary')">Summary</a></li>
        <li><a><button @click="logout" class="logout-btn">Logout</button></a></li>
      </ul>
    </nav>

    <!-- Page content -->
    <main class="content">
      
      <!-- Dashboard Summary Widget -->
      <section class="dashboard-summary">
        <h2>Parking Lots Summary</h2>
        <div class="summary-cards">
          <div class="card">
            <h3>Total Parking Lots</h3>
            <p>{{ stats.total_lots || 0 }}</p>
          </div>
          <div class="card">
            <h3>Total Spots</h3>
            <p>{{ stats.total_spots || 0 }}</p>
          </div>
          <div class="card">
            <h3>Available Spots</h3>
            <p>{{ stats.available_spots || 0 }}</p>
          </div>
        </div>
      </section>

      <!-- Manage Locations Section (Visible when Manage clicked) -->
      <section v-if="viewMode === 'manage'" class="mt-5">
        <h3>Manage Locations</h3>
        <div class="card shadow-sm mt-3">
          <div class="card-body p-0">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>Name</th>
                  <th>Address</th>
                  <th>Price/Hr</th>
                  <th>Capacity</th>
                  <th>Available</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="loc in locations" :key="loc.id">
                  <td>{{ loc.name }}</td>
                  <td>{{ loc.address }}</td>
                  <td>₹{{ loc.price }}</td>
                  <td>{{ loc.no_of_spots }}</td>
                  <td>{{ loc.available_spots }}</td>
                  <td>
                    <button @click="editLocation(loc)" class="btn btn-sm btn-outline-primary me-2">Edit</button>
                    <button @click="deleteLocation(loc.id)" class="btn btn-sm btn-outline-danger me-2">Delete</button>
                    <button @click="$router.push(`/admin/spots/${loc.id}`)" class="btn btn-sm btn-outline-success">View</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- Users Section -->
      <section v-if="viewMode === 'users'" class="mt-5">
        <h3>All Users</h3>
        <div class="card shadow-sm mt-3">
          <div class="card-body p-0">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.name }}</td>
                  <td>{{ user.email }}</td>
                  <td><span class="badge bg-info">{{ user.role }}</span></td>
                </tr>
                <tr v-if="users.length === 0">
                  <td colspan="4" class="text-center py-4">No users found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

    </main>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || showEditModal" class="modal-backdrop fade show"></div>
    <div v-if="showAddModal || showEditModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ showEditModal ? 'Edit Location' : 'Add New Location' }}</h5>
            <button @click="closeModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input v-model="form.name" type="text" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Address</label>
                <input v-model="form.address" type="text" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Pincode</label>
                <input v-model="form.pincode" type="text" class="form-control" required>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Price per Hour</label>
                  <input v-model="form.price" type="number" step="0.01" class="form-control" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Total Spots</label>
                  <input v-model="form.no_of_spots" type="number" class="form-control" required>
                </div>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" @click="closeModal" class="btn btn-secondary me-2">Cancel</button>
                <button type="submit" class="btn btn-primary">Save</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminPanel',
  data() {
    return {
      stats: {},
      locations: [],
      users: [],
      viewMode: 'dashboard', // dashboard, manage, users
      showAddModal: false,
      showEditModal: false,
      form: {
        id: null,
        name: '',
        address: '',
        pincode: '',
        price: '',
        no_of_spots: ''
      }
    }
  },
  async created() {
    await this.fetchSummary()
    await this.fetchLocations()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },
    async fetchUsers() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/customers', {
          headers: this.getHeaders()
        })
        this.users = res.data
      } catch (err) {
        console.error('Error loading users:', err)
      }
    },
    async fetchSummary() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/parking-summary', {
          headers: this.getHeaders()
        })
        this.stats = res.data
      } catch (err) {
        console.error('Error loading summary:', err)
      }
    },
    async fetchLocations() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/parkinglot', {
          headers: this.getHeaders()
        })
        this.locations = res.data.parking_lots
      } catch (err) {
        console.error('Error loading locations:', err)
      }
    },
    showManage() {
      this.viewMode = 'manage'
      this.fetchLocations()
    },
    showUsers() {
      this.viewMode = 'users'
      this.fetchUsers()
    },
    editLocation(loc) {
      this.form = { ...loc }
      this.showEditModal = true
    },
    closeModal() {
      this.showAddModal = false
      this.showEditModal = false
      this.form = { id: null, name: '', address: '', pincode: '', price: '', no_of_spots: '' }
    },
    async submitForm() {
      try {
        const url = this.showEditModal 
          ? `http://127.0.0.1:5000/api/parkinglot/${this.form.id}`
          : 'http://127.0.0.1:5000/api/parkinglot'
        
        const method = this.showEditModal ? 'put' : 'post'
        
        await axios[method](url, this.form, { headers: this.getHeaders() })
        
        await this.fetchLocations()
        await this.fetchSummary()
        this.closeModal()
      } catch (err) {
        alert(err.response?.data?.message || 'Operation failed')
      }
    },
    async deleteLocation(id) {
      if (!confirm('Are you sure?')) return
      try {
        await axios.delete(`http://127.0.0.1:5000/api/parkinglot/${id}`, { headers: this.getHeaders() })
        await this.fetchLocations()
        await this.fetchSummary()
      } catch (err) {
        alert(err.response?.data?.message || 'Delete failed')
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
/* Layout */
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f3f4f6;
}

/* Navbar */
.navbar {
  background-color: #2563eb;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.logo a {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 2rem;
  align-items: center;
  margin: 0;
  padding: 0;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  text-decoration: underline;
  color: #dbeafe;
}

/* Page Content */
.content {
  flex-grow: 1;
  padding: 2rem;
  background-color: #f9fafb;
}

/* Dashboard Summary Widget */
.dashboard-summary {
  margin-top: 2rem;
}

.dashboard-summary h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #1e40af;
}

.summary-cards {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.card {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgb(0 0 0 / 0.1);
  flex: 1 1 150px;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card h3 {
  margin-bottom: 0.5rem;
  color: #374151;
  font-weight: 600;
}

.logout-btn {
  background: transparent;
  border: none;
  color: white;
  font-weight: 500;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
}

.card p {
  font-size: 2rem;
  font-weight: bold;
  color: #2563eb;
}
</style>
