import { createRouter, createWebHistory } from 'vue-router'
///////////// MAIN LAYUOT ////////////
import mainLayout from '@/layout/mainLayout.vue'
///////////////// VIEWS ////////////////
import { Home } from '@/views'
import { forgetPassword, login, newPassword, singup, verifyCode } from '@/auth'
//////////////// STORE /////////////////
import { useUserStore } from '@/store/useUserStore'
import { CarUpload, EmailVeriy, profile } from '@/profile'
import ProfileLayout from '@/layout/profileLayout.vue'

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
          component: singup,
          meta: { guestOnly: true }
        },
        {
          path: "login",
          component: login,
          meta: { guestOnly: true }
        },
        {
          path: "forget",
          component: forgetPassword,
          meta: { guestOnly: true }
        },
        {
          path: "verify",
          component: verifyCode,
          meta: { verify: true }
        },
        {
          path: "newpass",
          component: newPassword,
          meta: { newpass: true }
        },
        {
          path: "",
          component: Home,
          name: "Home"
        },
        ///////// PROFILE ///////////
        {
          path: "profile",
          component: ProfileLayout,
          meta: { requiresAuth: true },
          children: [
            {
              path: "",
              component: profile,
              meta: { requiresAuth: true }
            }
          ]
        },
        {
          path: "email_verify",
          component: EmailVeriy,
          meta: { emailV: true }
        },
        {
          path: "upload",
          component: CarUpload,
          meta: { requiresAuth: true }
        }
      ]
    }
  ],
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const access_token = userStore.access_token
  const verify_token = userStore.verify_token
  const edit_password_token = userStore.edit_password_token
  const email_edit_token = userStore.email_edit_token

  if (to.meta.guestOnly && access_token) {
    return next("/")
  }

  if (to.meta.verify && !verify_token) {
    return next("/")
  }

  if (to.meta.newpass && !edit_password_token) {
    return next("/")
  }

  if (to.meta.emailV && !email_edit_token) {
    return next("/")
  }

  if (to.meta.requiresAuth && !access_token) {
    return next('/login')
  }


  next()
})

export default router
