import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Documents from '../views/Documents.vue'
import QA from '../views/QA.vue'
import KnowledgeBase from '../views/KnowledgeBase.vue'
import LearningPath from '../views/LearningPath.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { guestOnly: true },
    },
    {
      path: '/documents',
      name: 'documents',
      component: Documents,
      meta: { requiresAuth: true },
    },
    {
      path: '/qa',
      name: 'qa',
      component: QA,
      meta: { requiresAuth: true },
    },
    {
      path: '/knowledge',
      name: 'knowledge',
      component: KnowledgeBase,
      meta: { requiresAuth: true },
    },
    {
  path: '/learning-path',
  name: 'learning-path',
  component: LearningPath,
  meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  if (to.meta.guestOnly && token) {
    next('/')
    return
  }

  next()
})

export default router