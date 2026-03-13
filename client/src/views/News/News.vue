<template>
    <div class="container">
        <a-breadcrumb class="bread_crumb" separator=">">
            <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
            <a-breadcrumb-item><router-link to="/news">Новости</router-link></a-breadcrumb-item>
        </a-breadcrumb>
        <div class="news">
            <BlogSec :page_size="10"/>
        </div>
    </div>
</template>

<script setup>
import BlogSec from '../Home/BlogSec.vue';


</script>

<style scoped></style>