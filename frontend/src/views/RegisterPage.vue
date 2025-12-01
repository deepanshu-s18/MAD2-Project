<template>
  <div class="auth-container d-flex align-items-center justify-content-center">
    <div class="card shadow-lg p-4" style="width: 400px;">
      <h2 class="text-center mb-4">Create Account</h2>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" v-model="name" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Email Address</label>
          <input type="email" v-model="email" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Role</label>
          <select v-model="role" class="form-select">
            <option value="customer">Customer</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <button type="submit" class="btn btn-success w-100 mb-3">Register</button>
        <p class="text-center">
          Already have an account? <router-link to="/login">Login</router-link>
        </p>
      </form>
      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
      <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterPage',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      role: 'customer',
      error: '',
      success: ''
    }
  },
  methods: {
    async handleRegister() {
      try {
        await axios.post('http://127.0.0.1:5000/api/signup', {
          name: this.name,
          email: this.email,
          password: this.password,
          role: this.role
        })
        this.success = 'Registration successful! Redirecting...'
        setTimeout(() => this.$router.push('/login'), 1500)
      } catch (err) {
        this.error = err.response?.data?.message || 'Registration failed'
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  height: 100vh;
  background-color: #f0f2f5;
}
</style>
