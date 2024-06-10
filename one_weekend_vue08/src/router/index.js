import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import database_management from '../views/database_management.vue'
import database_file from '@/views/database_file.vue'
import file_block from '@/views/file_block.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/database_management',
      name: 'database_management',
      component: database_management

    },
    {
      path: '/database_file',
      name: 'database_file',
      component: database_file
    },
    {
      path: '/file_block',
      name: 'file_block',
      component: file_block
    }

  ]
})

export default router
