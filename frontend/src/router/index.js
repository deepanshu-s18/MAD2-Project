import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import AdminPanel from '../views/AdminPanel.vue'
import UserPanel from '../views/UserPanel.vue'
import UserSummary from '../views/UserSummary.vue'
import AdminSummary from '../views/AdminSummary.vue'
import AdminLocationSpots from '../views/AdminLocationSpots.vue'

const routes = [
    { path: '/', component: HomePage },
    { path: '/login', component: LoginPage },
    { path: '/register', component: RegisterPage },
    { path: '/admin', component: AdminPanel },
    { path: '/user', component: UserPanel },
    { path: '/user/summary', component: UserSummary },
    { path: '/admin/summary', component: AdminSummary },
    { path: '/admin/spots/:locationId', component: AdminLocationSpots }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
