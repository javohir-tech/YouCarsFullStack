<template>
    <div class="container">
        partners    
    </div>
</template>

<script setup>
import { useConversations } from '@/composables/useConversations';
import { onMounted } from 'vue';

const {isConnect , connect} = useConversations()

onMounted(()=>{
    connect()
})
</script>

<style scoped>
</style>