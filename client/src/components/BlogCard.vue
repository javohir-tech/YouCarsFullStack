<template>
    <div>
        <router-link class="blog_card" to="/">
            <div class="blog_image">
                <img :src="props.image" :alt="props.title">
            </div>
            <div class="car_info">
                <p class="title">{{ props.title }}</p>
                <p class="text">{{ props.text }}</p>
            </div>
            <div>
                Подробнее 
            </div>
        </router-link>
    </div>
</template>

<script setup>
const props = defineProps({
    image: String,
    text: String,
    title: String,
    id: String
})
</script>

<style scoped>
.blog_card {
    text-decoration: none;
}

.blog_image img {
    width: 100%;
    height: 250px;
    border-radius: 10px;
    object-position: center;
    object-fit: cover;
}

.car_info { 
    padding: 15px 10px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.title{
    font-weight: 500;
    font-size: 19px;
    color: rgba(41, 56, 67, 1);
}

.text{
    font-weight: 400;
    font-size: 15px;
    color: rgba(152, 152, 152, 1);
}
</style>