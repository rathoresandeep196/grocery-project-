<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <label for="username">Username:</label>
        <input type="text" v-model="username" required>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required>
        <button type="submit">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {

  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleLogin() {
      const formData = {
        username: this.username,
        password: this.password,
      };

      this.$axios.post("/login", formData)
        .then((response) => {
          const accessToken = response.data.access_token;
          localStorage.setItem("access_token", accessToken);
          const user = response.data.user;
          // localStorage.setItem("user", JSON.stringify(user));
          localStorage.setItem('userole', user.role);
          localStorage.setItem('isAuthenticated', true);
          

          // this.$store.commit('setAuthenticated', true);
          // this.toast.success('Login Successful', {
          //   position: 'top-right',
          //   duration: 5000,
          // });
          this.$router.push("/");
        })
        .catch((error) => {
    // console.error(error);
    let errorMessage = 'An unexpected error occurred';

    if (error.response) {
        if (error.response.data) {
            if (error.response.data.error) {
                errorMessage = error.response.data.error;
            } else {
                errorMessage = error.response.data.message || 'An error occurred';
            }
        } else {
            errorMessage = 'No response data';
        }
    } else if (error.message) {
        errorMessage = error.message;
    }
    console.log(errorMessage);

    // this.toast.error(errorMessage, {

    //     position: 'top-right',
    //     duration: 5000,
    // });
});


    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.login-form {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 400px;
}

h2 {
  margin-bottom: 16px;
  font-size: 24px;
}

label {
  font-size: 14px;
  font-weight: bold;
  display: block;
  margin-bottom: 6px;
}

input[type="text"],
input[type="password"] {
  width: 90%;
  padding: 10px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

button {
  background-color: #007bff;
  color: #ffffff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
