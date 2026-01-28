import { createRouter, createWebHistory } from 'vue-router'
///////////// MAIN LAYUOT ////////////
import mainLayout from '@/layout/mainLayout.vue'
///////////////// VIEWS ////////////////
import { Home } from '@/views'
import { forgetPassword, login, singup, verifyCode } from '@/auth'
import Profile from '@/profile/profile.vue'

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
          path: "forget",
          component: forgetPassword
        },
        {
          path: "verify", 
          component : verifyCode
        },
        {
          path: "",
          component: Home,
          name: "Home"
        },
        ///////// PROFILE ///////////
        {
          path: "profile",
          component: Profile
        }
      ]
    }
  ],
})

export default router
