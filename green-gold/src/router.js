import { createRouter, createWebHistory } from 'vue-router'
import StartPage from './components/StartPage.vue'
import MainPage from './components/MainPage.vue'
import AnjiTimeline from './components/AnjiTimeline.vue'
import QuizPage from './components/QuizPage.vue'
import KnowledgeMap from './components/KnowledgeMap.vue'
import CarbonCalculator from './components/CarbonCalculator.vue'

import SceneDesigner from './components/SceneDesigner.vue'
import WasteSortingGame from './components/WasteSortingGame.vue'

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
    },
    {
        path: '/carbon-calculator',
        component: CarbonCalculator
    },
    {
        path: '/scene-designer',
        component: SceneDesigner
    }
    ,
    {
        path: '/waste-sorting',
        component: WasteSortingGame
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router