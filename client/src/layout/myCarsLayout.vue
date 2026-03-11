<template>
    <div class="my-cars-container">
        <a-flex class="header" align="center" gap="10">
            <div class="back">
                <i class="fa-solid fa-angle-left" @click="toBack"></i>
            </div>
            <h1>Мои объявления</h1>
        </a-flex>

        <div class="tabs">
            <router-link to="/profile/mycars" class="tab-link" :class="{ active: isActive }">
                Активные
            </router-link>
            <router-link to="/profile/mycars/my_cars_arxiv" class="tab-link" :class="{ active: isArchive }">
                Архив
            </router-link>
        </div>

        <div class="tab-content">
            <router-view />
        </div>
    </div>
</template>

<script setup>
import router from '@/router'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const isActive = computed(() => {
    return route.path === '/profile/mycars'
})

const isArchive = computed(() => {
    return route.path === '/profile/mycars/my_cars_arxiv'
})

function toBack() {
    router.push("/profile")
}
</script>

<style scoped>
.header {
    padding-bottom: 10px;
    color: rgba(41, 56, 67, 1);
}

.header h1 {
    font-weight: 700;
    font-size: 30px;
    padding: 0;
    margin: 0;
}


.back i {
    font-size: 24px;
    color: rgba(41, 56, 67, 1);
}

.my-cars-container {
    padding: 0;
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
    color: rgba(38, 132, 229, 1);
    border-bottom-color: rgba(38, 132, 229, 1);
}

.tab-content {
    margin-top: 20px;
}

@media(max-width: 768px) {
    .my-cars-container {
        padding: 15px;
    }

    .header h1 {
        font-weight: 500;
        font-size: 22px;
    }

    .back {
        font-size: 22px;
    }
}

@media(min-width : 768px) {

    .back {
        display: none;
    }
}
</style>