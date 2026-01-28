import { createRouter, createWebHistory } from 'vue-router'
///////////// MAIN LAYUOT ////////////
import mainLayout from '@/layout/mainLayout.vue'
///////////////// VIEWS ////////////////
import { Home } from '@/views'
import { login, singup } from '@/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: mainLayout,
      children: [
        ////// AUTH /////
        {
          path: "singup",
          component: singup
        },
        {
          path: "login",
          component: login
        },
        {
          path: "",
          component: Home, 
          name : "Home"
        },
      ]
    }
  ],
})

export default router
