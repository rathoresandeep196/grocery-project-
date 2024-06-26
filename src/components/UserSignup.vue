<template>
  <div class="signup-container">
    <div class="signup-form">
      <h2>Sign Up</h2>
      <form @submit.prevent="signup">
        <label for="name">Name</label>
        <input type="text" id="name" v-model="name" required>
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required>
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      name: '',
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  methods: {
    checkEmailFormat(email) {
      const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return emailRegex.test(email);
    },
    signup() {
      if (this.password !== this.confirmPassword) {
        this.toast.error('Passwords do not match', {
          position: 'top-right',
          timeout: 5000,
        });
        return;
      }
      if (!this.checkEmailFormat(this.email)) {
        this.toast.error('Please enter a valid email address', {
          position: 'top-right',
          timeout: 5000,
        });
        return;
      }

      const formData = {
        name: this.name,
        username: this.username,
        email: this.email,
        password: this.password,
        confirmPassword: this.confirmPassword,
      };

      this.$axios
        .post('/signup', formData)
        .then(() => {
          this.$router.push('/login');
          this.toast.success('User Created Successfully', {
            position: 'top-right',
            timeout: 5000,
          });
        })
        .catch((error) => {
          if (error.response && error.response.data) {
            if (error.response.data.message === 'Username already exists') {
              this.toast.error('Username already exists', {
                position: 'top-right',
                timeout: 5000,
              });
            } else if (error.response.data.message === 'Email already exists') {
              this.toast.error('Email already exists', {
                position: 'top-right',
                timeout: 5000,
              });
            }
          } else {
            console.error(error);
            this.toast.error('An error occurred', {
              position: 'top-right',
              timeout: 5000,
            });
          }
        });
    },
  },
};
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.signup-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.signup-form h2 {
  margin-bottom: 20px;
}

.signup-form label {
  display: block;
  margin-bottom: 5px;
}

.signup-form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.signup-form button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.signup-form button:hover {
  background-color: #0056b3;
}
</style>
