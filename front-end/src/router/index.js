import { createRouter, createWebHistory } from 'vue-router';
import App from '@/App.vue'; // 默认页面
import LibraryPage from '@/components/LibraryPage.vue'; // LibraryPage 组件

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/App.vue'), // 默认加载 App 页面
  },
  {
    path: '/library',
    component: () => import('@/components/LibraryPage.vue')
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
