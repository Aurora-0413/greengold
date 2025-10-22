import { createRouter, createWebHistory } from 'vue-router'
import StartPage from './components/StartPage.vue'
import MainPage from './components/MainPage.vue'
import AnjiTimeline from './components/AnjiTimeline.vue'
import QuizPage from './components/QuizPage.vue'
import KnowledgeMap from './components/KnowledgeMap.vue'

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
    },
    {
        path: '/quiz',
        component: QuizPage
    },
    {
        path: '/knowledge',
        component: KnowledgeMap
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router