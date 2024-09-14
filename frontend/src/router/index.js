import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import SearchResults from '../views/SearchResults.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/search',
    name: 'SearchResults',
    component: SearchResults,
    props: route => ({ query: route.query.q })
  },
  // Add more routes as needed
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router