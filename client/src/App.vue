<script setup>
import { RouterView } from 'vue-router'
import axios from 'axios'
import { onMounted, onBeforeUnmount } from 'vue'
import { useUserStore } from './store/useUserStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

if (userStore.access_token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${userStore.access_token}`
}

const refreshAccessToken = async () => {
  const refresh_token = localStorage.getItem("refresh_token")
  if (!refresh_token) return

  try {
    const { data } = await axios.post(`${import.meta.env.VITE_API_URL}/auth/refresh/`, {
      refresh: refresh_token
    })

    userStore.add_access_token(data.access)
    localStorage.setItem("access_token", data.access)

    axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
  } catch (error) {
    console.log('Refresh token failed', error)
    localStorage.clear()
    userStore.clear()
    router.push("/login")
  }
}

let intervalId = null
const startTokenRefreshTimer = () => {
  intervalId = setInterval(() => {
    refreshAccessToken()
  }, 45 * 60 * 1000)
}
const stopTokenRefreshTimer = () => {
  if (intervalId) clearInterval(intervalId)
}

onMounted(() => {
  refreshAccessToken() 
  startTokenRefreshTimer() 
})

onBeforeUnmount(() => {
  stopTokenRefreshTimer()
})
</script>

<template>
  <RouterView />
</template>

<style scoped></style>
