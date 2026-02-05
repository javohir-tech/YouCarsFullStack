<template>
    <div class="my-cars-container">
        <h1 class="my_cars_header">Мои объявления</h1>
        
        <div class="tabs">
            <router-link 
                to="/profile/mycars" 
                class="tab-link"
                :class="{ active: isActive }"
            >
                Активные
            </router-link>
            <router-link 
                to="/profile/mycars/my_cars_arxiv" 
                class="tab-link"
                :class="{ active: isArchive }"
            >
                Архив
            </router-link>
        </div>
        
        <div class="tab-content">
            <router-view />
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const isActive = computed(() => {
    return route.path === '/profile/mycars'
})

const isArchive = computed(() => {
    return route.path === '/profile/mycars/my_cars_arxiv'
})
</script>

<style scoped>
.my-cars-container {
    padding: 20px;
}

.my_cars_header {
    font-size: 30px;
    font-weight: 600;
    color: #293843;
    margin-bottom: 20px;
}

.tabs {
    display: flex;
    gap: 30px;
    border-bottom: 2px solid #e5e7eb;
    margin-bottom: 30px;
}

.tab-link {
    padding: 12px 0;
    font-size: 16px;
    font-weight: 500;
    color: #6b7280;
    text-decoration: none;
    border-bottom: 3px solid transparent;
    transition: all 0.3s ease;
    position: relative;
    bottom: -2px;
}

.tab-link:hover {
    color: #293843;
}

.tab-link.active {
    color: #4f46e5;
    border-bottom-color: #4f46e5;
}

.tab-content {
    margin-top: 20px;
}
</style>