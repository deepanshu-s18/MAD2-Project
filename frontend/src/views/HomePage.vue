<template>
  <div class="home-container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="#">Parking System</a>
        <div class="d-flex">
          <router-link to="/login" class="btn btn-outline-light me-2">Login</router-link>
          <router-link to="/register" class="btn btn-primary">Register</router-link>
        </div>
      </div>
    </nav>

    <div class="hero-section text-center text-white d-flex align-items-center justify-content-center">
      <div class="content">
        <h1 class="display-3 fw-bold mb-4">Smart Parking Solution</h1>
        <p class="lead mb-5">Find and book parking spots with ease. Secure, fast, and reliable.</p>
        <router-link to="/login" class="btn btn-lg btn-success px-5">Get Started</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home-container {
  height: 100vh;
  background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1506521781263-d8422e82f27a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
  background-size: cover;
  background-position: center;
}

.hero-section {
  height: calc(100vh - 56px);
}
</style>
