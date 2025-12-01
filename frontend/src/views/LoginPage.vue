<template>
  <div class="auth-container d-flex align-items-center justify-content-center">
    <div class="card shadow-lg p-4" style="width: 400px;">
      <h2 class="text-center mb-4">Welcome Back</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">Email Address</label>
          <input type="email" v-model="email" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary w-100 mb-3">Login</button>
        <p class="text-center">
          New user? <router-link to="/register">Create account</router-link>
        </p>
      </form>
      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/login', {
          email: this.email,
          password: this.password
        })
        
        const { token, user_role, user_name } = response.data
        localStorage.setItem('token', token)
        localStorage.setItem('role', user_role)
        localStorage.setItem('user', user_name)
        
        if (user_role === 'admin') {
          this.$router.push('/admin')
        } else {
          this.$router.push('/user')
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Login failed'
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
