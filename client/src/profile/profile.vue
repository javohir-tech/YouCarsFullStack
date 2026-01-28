<template>
    profile
    <a-button :loading="loading" @click="handleLogOut">logout</a-button>
</template>

<script setup>
import api from '@/utils/axios';
import { message } from 'ant-design-vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/useUserStore';

const useStore = useUserStore()
const loading = ref(false)
const router = useRouter()
const handleLogOut = async () => {
    loading.value = true
    try {

        const refresh_token = localStorage.getItem('refresh_token')

        const { data } = await api.post('auth/logout/', {
            refresh: refresh_token
        })

        if (data.success) {
            localStorage.clear()
            useStore.clear()
            message.success(data.message)
            router.push("/")
        }
    } catch (error) {
        console.log(error)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped></style>