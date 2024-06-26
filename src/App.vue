<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <router-link to="/" class="nav-item">Home</router-link>
        <router-link v-if="!isAuthenticated" to="/login" class="nav-item">Login</router-link>
        <router-link v-if="!isAuthenticated" to="/signup" class="nav-item">Signup</router-link>
        <router-link v-if="isAuthenticated && isAdmin" to="/admin" class="nav-item">Admin</router-link>
        <router-link v-if="isAuthenticated && isAdmin" to="/productmanage" class="nav-item">manageProduct</router-link>
        <a v-if="isAuthenticated" @click="logout" class="nav-item" style="cursor: pointer;">Logout</a>
      </div>
    </nav>
    <div id="dashboard-postion">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: false,
      isAdmin: false
    };
  },
  created() {
    this.checkAuthentication();
  },
  methods: {
    checkAuthentication() {
      const authStatus = localStorage.getItem('isAuthenticated');
      const role = localStorage.getItem('userole');
      this.isAuthenticated = authStatus === 'true';
      this.isAdmin = role === 'admin';

      if (!this.isAuthenticated && this.$route.path !== '/login' && this.$route.path !== '/signup') {
        this.$router.push('/login');
      } else if (this.$route.path === '/admin' && !this.isAdmin) {
        this.$router.push('/login');
      }
    },
    logout() {
      localStorage.setItem('isAuthenticated', 'false');
      localStorage.removeItem('userRole'); // Clear the user role from localStorage
      this.isAuthenticated = false;
      this.isAdmin = false;
      this.$router.push('/login');
    }
  },
  watch: {
    $route() {
      this.checkAuthentication();
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.navbar {
  background-color: #6438c2;
  padding: 10px 0;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 50px;
  z-index: 1000;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-item {
  color: #fff;
  text-decoration: none;
  margin: 0 10px;
  font-family: Arial, Helvetica, sans-serif;
}

.nav-item:hover {
  text-decoration: underline;
}

#dashboard-postion {
  margin-top: 80px;
}
</style>
