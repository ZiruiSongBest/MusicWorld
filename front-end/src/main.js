import './assets/main.css'
import './assets/tailwind.css';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 引入路由

createApp(App).use(router).mount('#app'); // 使用路由
