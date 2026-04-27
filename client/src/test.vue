<template>
    <div v-for="user in data" :key="user.id" @click="handleClick">
        {{ user.username }}
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const data = ref([])

async function getData(){
    try {
        const response = await fetch("https://jsonplaceholder.typicode.com/users")
        console.log(response)
    } catch (error) {
        console.log(error)
    }
}

onMounted(()=>{
    getData()
})
</script>