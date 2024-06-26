import { createApp } from 'vue'
import App from './App.vue'
import router from './routes'
import axios from 'axios';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';


const app = createApp(App)


axios.defaults.baseURL = 'http://127.0.0.1:5000';

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000'
});





// Assign axiosInstance to global properties of the Vueapp
app.config.globalProperties.$axios = axiosInstance;

app.use(Toast, {
    // Optional configuration options
    position: 'top-right',
    timeout: 5000,
  });

app.use(router);

app.mount('#app')
