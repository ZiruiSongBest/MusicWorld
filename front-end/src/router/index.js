import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/components/Home.vue'),  // 默认加载 Home 组件
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('@/components/Library.vue'),  // 加载 Library 组件
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
