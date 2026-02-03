<template>
    <h1 class="my_cars_header">Мои объявления</h1>
    <router-link to="/profile/mycars">Активные</router-link> |
    <router-link to="/profile/mycars/my_cars_arxiv">Архив</router-link>
    <div>
        <router-view />
    </div>
</template>

<script setup>
</script>

<style scoped>
.my_cars_header{
    font-size: 30px;
    font-weight: 600;
    color: #293843;
}
</style>