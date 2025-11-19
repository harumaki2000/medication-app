import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AddMedication from '../views/AddMedication.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Login,
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/medications/add',
      name: 'add-medication',
      component: AddMedication
    }
  ],
})

export default router
