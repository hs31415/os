import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import dynamic from '../views/dynamic.vue'
import clock from '../views/clock.vue'
import show from '../views/show.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/dynamic',
      name: 'dynamic',
      component: dynamic
    },
    {
      path: '/clock',
      name: 'clock',
      component: clock
    },
    {
      path: '/show',
      name: 'show',
      component: show
    },
  ]
})

export default router
