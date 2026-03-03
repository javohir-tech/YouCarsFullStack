<template>
    <div class="container">
        chat
        <p>{{ route.params.userId }}</p>
        <p>{{ route.params.username }}</p>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { useChat } from '@/composables/useChat';
import { onMounted } from 'vue';

const route = useRoute()
const { message, isConnect, connect } = useChat(route.params.userId)

onMounted(() => {
    connect()
})
</script>

<style scoped></style>