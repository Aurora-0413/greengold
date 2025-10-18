import { createRouter, createWebHistory } from 'vue-router'
import StartPage from './components/StartPage.vue'
import MainPage from './components/MainPage.vue'

const routes = [
    {
        path: '/',
        component: StartPage
    },
    {
        path: '/main',
        component: MainPage
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router