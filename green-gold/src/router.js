import { createRouter, createWebHistory } from 'vue-router'
import StartPage from './components/StartPage.vue'
import MainPage from './components/MainPage.vue'
import AnjiTimeline from './components/AnjiTimeline.vue'

const routes = [
    {
        path: '/',
        component: StartPage
    },
    {
        path: '/main',
        component: MainPage
    },
    {
        path: '/anji-timeline',
        component: AnjiTimeline
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router