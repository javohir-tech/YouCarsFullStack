<template>
    my_cars_warehouse
</template>

<script setup>
import api from '@/utils/axios';
import { onMounted } from 'vue';


const getUserDraftCars = async () => {
    try {
        const data = await api.get("/cars/user/cars/draft/")

        console.log(data)
    } catch (error) {
        if (error.response) {
            console.log(error.response)
        } else {
            console.log(error.response)
        }
    }
}

onMounted(() => {
    getUserDraftCars()
})
</script>

<style scoped></style>